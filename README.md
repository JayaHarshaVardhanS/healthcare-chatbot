# Healthcare AI Assistant

A multi-agent healthcare analysis application built with **LangGraph**, **Retrieval-Augmented Generation (RAG)**, **ChromaDB**, and **Streamlit**.

The application analyzes an uploaded patient health report, retrieves relevant historical records for the selected patient, compares current values against prior measurements, and generates contextual health guidance.

> **Important:** This project uses synthetic patient data and is intended for demonstration and educational purposes only. It does not provide medical diagnosis and must not replace professional medical advice.

---

## Features

- Upload and parse PDF health reports
- Select a synthetic patient from the frontend
- Extract structured lab values and report metadata
- Retrieve patient-specific historical records using RAG
- Filter historical records by report date
- Compare current and previous health measurements
- Generate longitudinal trend analysis
- Produce structured observations and discussion points
- Automatic **Gemini → Groq** LLM fallback when Gemini quota/rate limits are reached
- Automatically initialize ChromaDB when the local vector database is missing
- Streamlit-based interactive user interface
- Synthetic patient records for safe testing and demonstration

---

## Architecture

```text
                  Uploaded PDF Report
                         │
                         ▼
                    PDF Parser
                         │
                         ▼
                  Report Analyzer
                         │
                         ▼
                  LangGraph State
                         │
                         ▼
                    Health Agent
                         │
                         ▼
                      RAG Tool
                         │
                         ▼
              Patient-filtered ChromaDB
                         │
                         ▼
               Historical Medical Records
                         │
                         ▼
                  Comparison Agent
                         │
                         ▼
               Longitudinal Trend Analysis
                         │
                         ▼
               Recommendation Agent
                         │
                         ▼
                  Streamlit Results
```

### LLM failover

```text
Agent request
     │
     ▼
   Gemini
     │
     ├── Success ─────────────► Structured response
     │
     └── 429 / quota exceeded
                │
                ▼
              Groq
                │
                ▼
        Structured response
```

---

## Project Structure

```text
healthcare-chatbot/
│
├── app/
│   ├── __init__.py
│   │
│   ├── graph/
│   │   ├── __init__.py
│   │   ├── state.py
│   │   ├── graph.py
│   │   ├── nodes.py
│   │   └── prompts.py
│   │
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── health_agent.py
│   │   ├── recommendation_agent.py
│   │   └── report_analyzer.py
│   │
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── rag_tool.py
│   │   ├── comparision_tool.py
│   │   └── report_parser.py
│   │
│   ├── rag/
│   │   ├── __init__.py
│   │   ├── ingestion.py
│   │   ├── embeddings.py
│   │   └── retriever.py
│   │
│   ├── llm/
│   │   ├── __init__.py
│   │   └── provider.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py
│   │
│   └── config.py
│
├── data/
│   ├── generate_patient_history.py
│   └── patient_records/
│
├── tests/
│   └── test_graph.py
│
├── .gitignore
├── pyproject.toml
├── uv.lock
├── main.py
└── streamlit_app.py
```

> The current codebase uses `comparision_tool.py`. It can optionally be renamed later to `comparison_tool.py` for spelling consistency.

---

## Technology Stack

### AI / Orchestration

- LangGraph
- LangChain
- Google Gemini
- Groq

### Retrieval

- ChromaDB
- LangChain Chroma
- Vector embeddings

### Backend

- Python
- Pydantic

### Frontend

- Streamlit

### Package Management

- uv

---

## Synthetic Patients

The demo includes five synthetic patients:

| Patient ID | Demo focus |
|---|---|
| `P001` | Glucose, HbA1c, cholesterol, triglycerides |
| `P002` | Hemoglobin and ferritin |
| `P003` | Blood pressure and LDL cholesterol |
| `P004` | Vitamin D, Vitamin B12, and hemoglobin |
| `P005` | Lipid profile |

When testing the application, select the Patient ID that corresponds to the uploaded test report.

---

## How the RAG Pipeline Works

Historical patient records are indexed into ChromaDB with metadata such as:

```python
{
    "patient_id": "P001",
    "record_date": "2025-08-10",
    "source": "2025-08-10_lab_report.txt",
    "document_type": "lab_report"
}
```

When a current report is uploaded, the application:

1. Extracts the report date and current health values.
2. Uses the Patient ID selected in the frontend.
3. Retrieves only records belonging to that patient.
4. Excludes records dated on or after the current report date.
5. Passes the historical records to the comparison agent.
6. Generates a chronological interpretation of the patient's health trends.

This prevents the current report from being compared against itself.

---

## ChromaDB Auto-Initialization

The generated local Chroma database is intentionally not committed to GitHub.

```text
chroma_db/
```

is excluded through `.gitignore`.

If the application starts and the Chroma collection is missing or empty, the application automatically creates the vector database from:

```text
data/patient_records/
```

This makes the project reproducible in cloud environments such as Streamlit Community Cloud.

---

## Prerequisites

- Python 3.11+ recommended
- uv
- Google Gemini API key
- Groq API key

---

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/healthcare-chatbot.git
cd healthcare-chatbot
```

Install dependencies using uv:

```bash
uv sync
```

---

## Environment Variables

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_google_api_key
GROQ_API_KEY=your_groq_api_key

LLM_MODEL=gemini-2.5-flash
GROQ_MODEL=openai/gpt-oss-120b
```

Do not commit `.env` to source control.

---

## Run the Streamlit Application

Using uv:

```bash
uv run streamlit run streamlit_app.py
```

Then open the local Streamlit URL shown in your terminal.

---

## Run the Backend Workflow Directly

The LangGraph workflow can also be tested without the UI:

```bash
uv run python main.py
```

---

## Generate Synthetic Patient Records

If the test records need to be regenerated:

```bash
uv run python data/generate_patient_history.py
```

The historical records are created under:

```text
data/patient_records/
```

---

## Rebuild ChromaDB Manually

The application initializes Chroma automatically, but it can also be recreated manually.

Delete the existing local database:

### Windows PowerShell

```powershell
Remove-Item -Recurse -Force .\chroma_db
```

Then start the application again, or run the ingestion module directly if desired.

---

## Streamlit Community Cloud Deployment

1. Push the project to GitHub.
2. Open Streamlit Community Cloud.
3. Create a new application from the GitHub repository.
4. Select:

```text
Branch: main
Main file: streamlit_app.py
```

5. Add the required secrets in Streamlit Cloud:

```toml
GOOGLE_API_KEY = "your_google_api_key"
GROQ_API_KEY = "your_groq_api_key"

LLM_MODEL = "gemini-2.5-flash"
GROQ_MODEL = "openai/gpt-oss-120b"
```

6. Deploy the application.

Because ChromaDB is initialized automatically, the deployed application can rebuild its vector database from the synthetic records included in the repository.

---

## Example Workflow

```text
1. Select P003
2. Upload the P003 test report
3. Click Analyze Health Report
4. Report Analyzer extracts current values
5. RAG retrieves P003 historical records
6. Comparison Agent identifies trends
7. Recommendation Agent generates health guidance
8. Results are displayed in Streamlit
```

---

## Safety and Medical Disclaimer

This project is a technical demonstration.

- All included patients and medical records are synthetic.
- The application is not a medical device.
- Outputs should not be used for diagnosis or treatment.
- AI-generated content can be incomplete or incorrect.
- Medical decisions should always be discussed with a qualified healthcare professional.

---

## Future Improvements

Possible future enhancements include:

- Interactive longitudinal charts for biomarkers
- Authentication and patient authorization
- Support for additional document types
- More robust medical document parsing
- Improved structured medical terminology
- Persistent cloud vector storage
- LLM provider telemetry and fallback visibility
- Automated evaluation of RAG retrieval quality
- Unit and integration test coverage
- FastAPI backend with a separate React/Next.js frontend
- FHIR-compatible patient data integration

---

## Portfolio Summary

This project demonstrates:

- Multi-agent AI orchestration with LangGraph
- Retrieval-Augmented Generation
- Patient-specific vector retrieval
- Metadata-based filtering
- Longitudinal healthcare data analysis
- Structured LLM outputs with Pydantic
- Multi-provider LLM resilience
- Streamlit application development
- Reproducible cloud deployment
- Safe synthetic healthcare data design

---

## License

This project is intended for educational and portfolio use.

