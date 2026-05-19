import sys
import os

def extract_text(pdf_path, start_page=None, end_page=None):
    try:
        from pypdf import PdfReader
        reader = PdfReader(pdf_path)
        text = ""
        
        start_idx = 0 if start_page is None else max(0, start_page - 1)
        end_idx = len(reader.pages) if end_page is None else min(len(reader.pages), end_page)
        
        for i in range(start_idx, end_idx):
            page = reader.pages[i]
            text += f"\n--- Page {i+1} ---\n"
            page_text = page.extract_text()
            if page_text:
                text += page_text
        return text
    except ImportError:
        return "Error: pypdf is not installed. Please run: pip install pypdf"
    except Exception as e:
        return f"Error extracting text: {e}"

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python extract_pdf.py <path_to_pdf> <output_txt_path>")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    out_path = sys.argv[2]
    
    if not os.path.exists(pdf_path):
        print(f"Error: PDF not found at {pdf_path}")
        sys.exit(1)
        
    text = extract_text(pdf_path)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Extraction saved to {out_path}")
