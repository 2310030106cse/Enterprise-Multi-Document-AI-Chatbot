from src.pdf_loader import extract_text_from_pdf
from src.text_splitter import split_text

pdf_path = "data/sample.pdf"

text = extract_text_from_pdf(pdf_path)

chunks = split_text(text)

print("=" * 50)
print("TOTAL CHUNKS:", len(chunks))
print("=" * 50)

for i, chunk in enumerate(chunks):
    print(f"\nChunk {i+1}")
    print("-" * 40)
    print(chunk)