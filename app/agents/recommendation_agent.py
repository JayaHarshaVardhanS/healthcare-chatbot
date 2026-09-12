from app.graph.prompts import (
    RECOMMENDATION_PROMPT,
)

from app.models.schemas import (
    RecommendationResult,
)

from app.llm.provider import (
    invoke_with_fallback,
)


def generate_recommendations(
    current_report: dict,
    historical_records: list,
    comparison: dict,
) -> RecommendationResult:

    prompt = RECOMMENDATION_PROMPT.format(
        current_report=current_report,
        historical_records=historical_records,
        comparison=comparison,
    )

    print(
        "\nGenerating recommendations..."
    )

    result = invoke_with_fallback(
        prompt=prompt,
        output_schema=RecommendationResult,
    )

    if not isinstance(
        result,
        RecommendationResult,
    ):
        raise TypeError(
            "Unexpected recommendation "
            "response type: "
            f"{type(result)}"
        )

    return result