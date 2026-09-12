from app.tools.rag_tool import (
    retrieve_patient_history
)
from dotenv import load_dotenv
load_dotenv()


def main():

    results = retrieve_patient_history(
        patient_id="P001",
        query=(
            "previous HbA1c results "
            "and diabetes prescriptions"
        ),
        k=5
    )

    for index, result in enumerate(
        results,
        start=1
    ):

        print("\n" + "=" * 60)

        print(
            f"RESULT {index}"
        )

        print(
            "\nMetadata:"
        )

        print(
            result["metadata"]
        )

        print(
            "\nContent:"
        )

        print(
            result["content"]
        )


if __name__ == "__main__":
    main()