import fitz
import os

pdf_path = r'y:\Hunter\eco331\read\atack-et-al-2019-automation.pdf'
out_dir = r'y:\Hunter\eco331\read\atack_images'
os.makedirs(out_dir, exist_ok=True)

doc = fitz.open(pdf_path)
count = 0
for i, page in enumerate(doc):
    pix = page.get_pixmap(dpi=300)
    img_filename = os.path.join(out_dir, f'page_{i+1}.png')
    pix.save(img_filename)
    count += 1

print(f"Rendered {count} pages to images")
