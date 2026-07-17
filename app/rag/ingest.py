from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter

document_path = Path("documents/tenant_manual.txt")

text = document_path.read_text()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,
    chunk_overlap=50
)

chunks = text_splitter.split_text(text)

for index, chunk in enumerate(chunks):

    print("=" * 60)
    print(f"Chunk {index + 1}")
    print("=" * 60)
    print(chunk)