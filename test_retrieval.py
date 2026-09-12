from app.tools.rag_tool import retrieve_patient_history

patient_id = "P002"

query = """
Find historical laboratory reports for this patient,
especially HbA1c, fasting glucose, LDL cholesterol,
HDL cholesterol and triglycerides.
"""

results = retrieve_patient_history(
    patient_id=patient_id,
    query=query,
    current_report_date="2026-03-12",
    k=5
)

print("=" * 60)
print("RAG RETRIEVAL TEST")
print("=" * 60)

print(f"\nRetrieved {len(results)} documents.")

for i, result in enumerate(results, start=1):
    print(f"\n--- Document {i} ---")
    print("Metadata:")
    print(result.metadata)

    print("\nContent:")
    print(result["content"][:1000])