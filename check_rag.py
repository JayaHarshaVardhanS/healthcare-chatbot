from app.rag.retriever import get_vectorstore

vectorstore = get_vectorstore()

collection = vectorstore._collection

print("=" * 60)
print("CHROMA COLLECTION CHECK")
print("=" * 60)

print("\nCollection name:")
print(collection.name)

print("\nDocument count:")
print(collection.count())

print("\nSample records:")

result = collection.get(
    limit=10,
    include=["documents", "metadatas"]
)

for i, (doc, metadata) in enumerate(
    zip(result["documents"], result["metadatas"])
):
    print(f"\n--- Record {i + 1} ---")
    print("Metadata:", metadata)
    print("Document:", doc[:300])