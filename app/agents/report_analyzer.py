from app.models.schemas import ReportAnalysis
from app.graph.prompts import REPORT_ANALYSIS_PROMPT
from app.llm.provider import invoke_with_fallback


def analyze_health_report(
    report: str
) -> ReportAnalysis:

    prompt = REPORT_ANALYSIS_PROMPT.format(
        report=report
    )

    print("\nAnalyzing uploaded health report...")

    result = invoke_with_fallback(
        prompt=prompt,
        output_schema=ReportAnalysis,
    )

    if result is None:
        raise ValueError(
            "Report analysis returned None."
        )

    if not isinstance(
        result,
        ReportAnalysis
    ):
        raise TypeError(
            "Unexpected report analysis "
            f"response type: {type(result)}"
        )

    return result