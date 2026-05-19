"""
embed_html_images.py
--------------------
Post-processes Marp-generated HTML files to embed all local images
as base64 data URIs, producing a single fully self-contained HTML file.

Usage:
    python code/embed_html_images.py                  # embeds all slides/html/*.html
    python code/embed_html_images.py slides/html/sl_4_Malthus.html  # single file

Output: overwrites each HTML file in-place (or pass --suffix to keep originals).
"""

import re
import base64
import sys
from pathlib import Path
from urllib.parse import unquote

MIME_TYPES = {
    ".png":  "image/png",
    ".jpg":  "image/jpeg",
    ".jpeg": "image/jpeg",
    ".gif":  "image/gif",
    ".svg":  "image/svg+xml",
    ".webp": "image/webp",
    ".bmp":  "image/bmp",
}


def to_data_uri(file_path: Path) -> str:
    mime = MIME_TYPES.get(file_path.suffix.lower(), "image/png")
    data = base64.b64encode(file_path.read_bytes()).decode("utf-8")
    return f"data:{mime};base64,{data}"


def embed_images(html_path: Path, suffix: str = "") -> Path:
    html_dir = html_path.parent
    content = html_path.read_text(encoding="utf-8")
    replaced = skipped = 0

    def replace_ref(url: str) -> str | None:
        """Return data URI if url is a resolvable local file, else None."""
        nonlocal replaced, skipped
        if url.startswith(("data:", "http://", "https://", "//")):
            return None
        candidate = (html_dir / unquote(url)).resolve()
        if candidate.exists():
            replaced += 1
            return to_data_uri(candidate)
        skipped += 1
        print(f"  [missing] {url}")
        return None

    # CSS url() references  (background-image, etc.)
    # Marp HTML-escapes the quotes as &quot; inside url(), so handle both forms
    def sub_css_url(m):
        raw = m.group(1).strip("\"'").replace("&quot;", "")
        uri = replace_ref(raw)
        return f"url(&quot;{uri}&quot;)" if uri else m.group(0)

    # Match both url("...") and url(&quot;...&quot;) forms
    content = re.sub(r'url\(\s*(?:&quot;|["\'])?([^)&"\']+)(?:&quot;|["\'])?\s*\)', sub_css_url, content)

    # <img src="..."> and similar src= attributes
    def sub_src(m):
        url = m.group(1)
        uri = replace_ref(url)
        return f'src="{uri}"' if uri else m.group(0)

    content = re.sub(r'src="([^"]+)"', sub_src, content)

    out_path = html_path.with_stem(html_path.stem + suffix) if suffix else html_path
    out_path.write_text(content, encoding="utf-8")
    print(f"  {html_path.name} -> {out_path.name}  ({replaced} embedded, {skipped} missing)")
    return out_path


def main():
    args = sys.argv[1:]
    suffix = ""

    # Optional --suffix flag
    if "--suffix" in args:
        idx = args.index("--suffix")
        suffix = args[idx + 1]
        args = [a for i, a in enumerate(args) if i not in (idx, idx + 1)]

    if args:
        targets = [Path(a) for a in args]
    else:
        # Default: all HTML files in slides/html/
        root = Path(__file__).parent.parent  # eco331/
        targets = sorted((root / "slides" / "html").glob("*.html"))

    print(f"Embedding images in {len(targets)} file(s)...")
    for p in targets:
        embed_images(p, suffix=suffix)
    print("Done.")


if __name__ == "__main__":
    main()
