from pathlib import Path
from datetime import date

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


OUTPUT_DIR = Path(
    "data/patient_records"
)


PATIENTS = {

    "P001": {
        "name": "Patient Alpha",
        "age": 52,
        "gender": "Male"
    },

    "P002": {
        "name": "Patient Beta",
        "age": 44,
        "gender": "Female"
    },

    "P003": {
        "name": "Patient Gamma",
        "age": 61,
        "gender": "Male"
    },

    "P004": {
        "name": "Patient Delta",
        "age": 36,
        "gender": "Female"
    },

    "P005": {
        "name": "Patient Epsilon",
        "age": 68,
        "gender": "Male"
    }
}


HISTORY = {

    "P001": [

        {
            "date": "2024-01-15",

            "type": "visit",

            "content": """
Patient: P001
Visit Date: 2024-01-15

Reason for visit:
Routine metabolic health evaluation.

Observations:
Fasting glucose: 168 mg/dL
HbA1c: 8.1 %
LDL cholesterol: 152 mg/dL
HDL cholesterol: 39 mg/dL
Triglycerides: 188 mg/dL

Assessment documented by physician:
Elevated glucose and HbA1c were documented.
Dyslipidemia was also documented.

Prescription:
Metformin 500 mg once daily with food.

Follow-up:
Repeat laboratory evaluation recommended.
"""
        },

        {
            "date": "2024-06-20",

            "type": "lab_report",

            "content": """
Patient: P001
Lab Report Date: 2024-06-20

Laboratory results:

Fasting glucose: 151 mg/dL
HbA1c: 7.7 %
LDL cholesterol: 145 mg/dL
HDL cholesterol: 41 mg/dL
Triglycerides: 170 mg/dL

Historical comparison:
HbA1c was previously documented as 8.1 %.

No medication change documented in this report.
"""
        },

        {
            "date": "2024-06-22",

            "type": "prescription",

            "content": """
Patient: P001
Prescription Date: 2024-06-22

Medication:
Metformin 500 mg once daily.

Instruction:
Continue medication as prescribed.

Follow-up:
Repeat HbA1c and metabolic panel at next review.
"""
        },

        {
            "date": "2025-01-18",

            "type": "lab_report",

            "content": """
Patient: P001
Lab Report Date: 2025-01-18

Laboratory results:

Fasting glucose: 139 mg/dL
HbA1c: 7.3 %
LDL cholesterol: 138 mg/dL
HDL cholesterol: 44 mg/dL
Triglycerides: 158 mg/dL

Historical HbA1c:
2024-01-15: 8.1 %
2024-06-20: 7.7 %
Current: 7.3 %

The report documents continued monitoring.
"""
        },

        {
            "date": "2025-01-20",

            "type": "prescription",

            "content": """
Patient: P001
Prescription Date: 2025-01-20

Medication:
Metformin 500 mg once daily.

No medication dose change documented.

Follow-up:
Continue periodic laboratory monitoring.
"""
        },

        {
            "date": "2025-08-10",

            "type": "lab_report",

            "content": """
Patient: P001
Lab Report Date: 2025-08-10

Laboratory results:

Fasting glucose: 128 mg/dL
HbA1c: 6.9 %
LDL cholesterol: 125 mg/dL
HDL cholesterol: 47 mg/dL
Triglycerides: 142 mg/dL

The laboratory report shows HbA1c of 6.9 %.
Previous HbA1c was 7.3 %.
"""
        },

        {
            "date": "2026-03-12",

            "type": "lab_report",

            "content": """
Patient: P001
Lab Report Date: 2026-03-12

Laboratory results:

Fasting glucose: 142 mg/dL
HbA1c: 7.4 %
LDL cholesterol: 131 mg/dL
HDL cholesterol: 45 mg/dL
Triglycerides: 150 mg/dL

"""
        }
    ],

    "P002": [

        {
            "date": "2024-02-10",
            "type": "visit",
            "content": """
Patient: P002
Visit Date: 2024-02-10

Reason:
Annual health evaluation.

Laboratory results:
Hemoglobin: 11.2 g/dL
Ferritin: 12 ng/mL
Vitamin B12: 310 pg/mL

Assessment:
Low hemoglobin and low ferritin documented.

Prescription:
Oral iron supplementation was prescribed.

Follow-up:
Repeat CBC and ferritin recommended.
"""
        },

        {
            "date": "2024-08-14",
            "type": "lab_report",
            "content": """
Patient: P002
Lab Report Date: 2024-08-14

Hemoglobin: 11.8 g/dL
Ferritin: 21 ng/mL
Vitamin B12: 328 pg/mL

Previous hemoglobin:
11.2 g/dL.

The report documents improvement in hemoglobin.
"""
        },

        {
            "date": "2025-02-15",
            "type": "lab_report",
            "content": """
Patient: P002
Lab Report Date: 2025-02-15

Hemoglobin: 12.3 g/dL
Ferritin: 34 ng/mL
Vitamin B12: 355 pg/mL

Previous hemoglobin:
11.8 g/dL.

No new medication change documented.
"""
        },

        {
            "date": "2025-09-18",
            "type": "visit",
            "content": """
Patient: P002
Visit Date: 2025-09-18

Reason:
Follow-up laboratory review.

Hemoglobin: 12.5 g/dL
Ferritin: 39 ng/mL

Previous supplementation documented.

Plan:
Continue follow-up according to treating physician.
"""
        }
    ],

    "P003": [

        {
            "date": "2024-03-11",
            "type": "visit",
            "content": """
Patient: P003
Visit Date: 2024-03-11

Blood pressure:
148/92 mmHg

LDL cholesterol:
168 mg/dL

Assessment:
Elevated blood pressure and LDL cholesterol
were documented.

Prescription:
Antihypertensive medication initiated.

Lifestyle counselling documented.
"""
        },

        {
            "date": "2024-10-11",
            "type": "lab_report",
            "content": """
Patient: P003
Lab Report Date: 2024-10-11

Blood pressure at visit:
139/86 mmHg

LDL cholesterol:
151 mg/dL

Previous LDL:
168 mg/dL.

The report documents lower LDL compared with
the previous measurement.
"""
        },

        {
            "date": "2025-05-20",
            "type": "lab_report",
            "content": """
Patient: P003
Lab Report Date: 2025-05-20

Blood pressure:
134/82 mmHg

LDL cholesterol:
132 mg/dL

The report documents continued monitoring.
"""
        },

        {
            "date": "2026-02-05",
            "type": "lab_report",
            "content": """
Patient: P003
Lab Report Date: 2026-02-05

Blood pressure:
142/88 mmHg

LDL cholesterol:
139 mg/dL

Previous LDL:
132 mg/dL.

The report documents an increase in LDL compared
with the previous measurement.
"""
        }
    ],

    "P004": [

        {
            "date": "2024-04-05",
            "type": "visit",
            "content": """
Patient: P004
Visit Date: 2024-04-05

Reason:
Fatigue evaluation.

Laboratory results:
Vitamin D: 16 ng/mL
Vitamin B12: 280 pg/mL
Hemoglobin: 12.1 g/dL

The report documents low Vitamin D.

Supplementation was discussed.
"""
        },

        {
            "date": "2024-11-12",
            "type": "lab_report",
            "content": """
Patient: P004
Lab Report Date: 2024-11-12

Vitamin D: 27 ng/mL
Vitamin B12: 315 pg/mL
Hemoglobin: 12.4 g/dL

Previous Vitamin D:
16 ng/mL.

The report documents an increase in Vitamin D.
"""
        },

        {
            "date": "2025-07-22",
            "type": "lab_report",
            "content": """
Patient: P004
Lab Report Date: 2025-07-22

Vitamin D: 34 ng/mL
Vitamin B12: 342 pg/mL
Hemoglobin: 12.7 g/dL

Previous Vitamin D:
27 ng/mL.

Continued monitoring documented.
"""
        }
    ],

    "P005": [

        {
            "date": "2024-01-25",
            "type": "visit",
            "content": """
Patient: P005
Visit Date: 2024-01-25

Reason:
Cardiometabolic health evaluation.

Total cholesterol: 246 mg/dL
LDL cholesterol: 174 mg/dL
HDL cholesterol: 36 mg/dL
Triglycerides: 210 mg/dL

Assessment:
Elevated lipid measurements documented.

Prescription:
Lipid-lowering medication prescribed.

Follow-up:
Repeat lipid profile recommended.
"""
        },

        {
            "date": "2024-09-30",
            "type": "lab_report",
            "content": """
Patient: P005
Lab Report Date: 2024-09-30

Total cholesterol: 208 mg/dL
LDL cholesterol: 139 mg/dL
HDL cholesterol: 41 mg/dL
Triglycerides: 172 mg/dL

Previous LDL:
174 mg/dL.

The report documents lower LDL.
"""
        },

        {
            "date": "2025-06-14",
            "type": "lab_report",
            "content": """
Patient: P005
Lab Report Date: 2025-06-14

Total cholesterol: 196 mg/dL
LDL cholesterol: 126 mg/dL
HDL cholesterol: 44 mg/dL
Triglycerides: 151 mg/dL

Previous LDL:
139 mg/dL.

The report documents continued improvement.
"""
        },

        {
            "date": "2026-04-02",
            "type": "lab_report",
            "content": """
Patient: P005
Lab Report Date: 2026-04-02

Total cholesterol: 214 mg/dL
LDL cholesterol: 142 mg/dL
HDL cholesterol: 42 mg/dL
Triglycerides: 166 mg/dL

Previous LDL:
126 mg/dL.

The report documents an increase in LDL.
"""
        }
    ]
}


def create_txt_file(
    patient_id: str,
    record: dict
):

    patient_dir = (
        OUTPUT_DIR / patient_id
    )

    patient_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    filename = (
        f"{record['date']}_"
        f"{record['type']}.txt"
    )

    path = patient_dir / filename

    path.write_text(
        record["content"].strip(),
        encoding="utf-8"
    )


def create_pdf_file(
    patient_id: str,
    record: dict
):

    patient_dir = (
        OUTPUT_DIR / patient_id
    )

    patient_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    filename = (
        f"{record['date']}_"
        f"{record['type']}.pdf"
    )

    path = patient_dir / filename

    pdf = canvas.Canvas(
        str(path),
        pagesize=A4
    )

    width, height = A4

    x = 50
    y = height - 50

    pdf.setFont(
        "Helvetica",
        10
    )

    for line in record["content"].strip().split("\n"):

        line = line.strip()

        if not line:
            y -= 10
            continue

        # Basic page handling
        if y < 50:

            pdf.showPage()

            pdf.setFont(
                "Helvetica",
                10
            )

            y = height - 50

        pdf.drawString(
            x,
            y,
            line[:110]
        )

        y -= 15

    pdf.save()


def create_demographics(
    patient_id: str,
    patient: dict
):

    patient_dir = (
        OUTPUT_DIR / patient_id
    )

    patient_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    content = f"""
Patient ID: {patient_id}
Name: {patient['name']}
Age: {patient['age']}
Gender: {patient['gender']}

This is a synthetic patient record created
for testing a healthcare RAG application.

This record does not represent a real person.
"""

    path = patient_dir / "demographics.txt"

    path.write_text(
        content.strip(),
        encoding="utf-8"
    )


def generate_data():

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    for patient_id, patient in PATIENTS.items():

        print(
            f"Generating records for {patient_id}"
        )

        create_demographics(
            patient_id,
            patient
        )

        for record in HISTORY[patient_id]:

            create_txt_file(
                patient_id,
                record
            )

            create_pdf_file(
                patient_id,
                record
            )

    print(
        "\nSynthetic patient history generated."
    )


if __name__ == "__main__":
    generate_data()