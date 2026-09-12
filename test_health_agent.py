from app.agents.health_agent import run_health_agent

report_analysis = {
    "report_date": "2026-03-12",
    "conditions": [],
    "medications": [],
    "symptoms": [],
    "lab_values": [
        {
            "name": "Fasting glucose",
            "value": 142.0,
            "unit": "mg/dL"
        },
        {
            "name": "HbA1c",
            "value": 7.4,
            "unit": "%"
        },
        {
            "name": "LDL cholesterol",
            "value": 131.0,
            "unit": "mg/dL"
        },
        {
            "name": "HDL cholesterol",
            "value": 45.0,
            "unit": "mg/dL"
        },
        {
            "name": "Triglycerides",
            "value": 150.0,
            "unit": "mg/dL"
        }
    ],
    "important_findings": [
        "Increase in HbA1c compared with the previous result"
    ]
}

print("=" * 60)
print("HEALTH AGENT TEST")
print("=" * 60)

documents = run_health_agent(
    patient_id="P001",
    report_analysis=report_analysis
)

print(f"\nFinal result: {len(documents)} documents")

for i, doc in enumerate(documents, 1):
    print(f"\n--- Document {i} ---")
    print(doc["metadata"])
    print(doc["content"][:500])