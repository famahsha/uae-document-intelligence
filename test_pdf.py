import fitz  # pymupdf

# Open the PDF
doc = fitz.open("rag/documents/uae_labour_law.pdf")

print(f"Total pages: {len(doc)}")

# Read first page
page = doc[0]
text = page.get_text()

print("\nFirst page sample:")
print(text[:500])