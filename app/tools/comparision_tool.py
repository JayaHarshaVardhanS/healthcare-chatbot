from app.graph.prompts import (
    COMPARISON_PROMPT,
)

from app.models.schemas import (
    ComparisonResult,
)

from app.llm.provider import (
    invoke_with_fallback,
)


def compare_reports(
    current_report: dict,
    historical_records: list,
):

    prompt = COMPARISON_PROMPT.format(
        current_report=current_report,
        historical_records=historical_records,
    )

    result = invoke_with_fallback(
        prompt=prompt,
        output_schema=ComparisonResult,
    )

    if not isinstance(
        result,
        ComparisonResult,
    ):
        raise TypeError(
            "Unexpected comparison response "
            f"type: {type(result)}"
        )

    return result.model_dump()


def comparison_tool_definition():

    return {
        "name": "compare_reports",
        "description": (
            "Compare the current patient report "
            "against historical patient records."
        ),
    }