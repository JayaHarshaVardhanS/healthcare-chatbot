import streamlit as st
import tempfile
import os

from app.graph.graph import healthcare_graph
from app.tools.report_parser import parse_pdf


# ============================================================
# Page Configuration
# ============================================================

st.set_page_config(
    page_title="Healthcare AI Assistant",
    page_icon="🏥",
    layout="wide",
)


# ============================================================
# Styling
# ============================================================

st.markdown(
    """
    <style>

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }

    .app-subtitle {
        font-size: 1.05rem;
        color: #6b7280;
        margin-bottom: 1.5rem;
    }

    .section-card {
        padding: 1.2rem;
        border: 1px solid rgba(128, 128, 128, 0.25);
        border-radius: 12px;
        margin-bottom: 1rem;
    }

    .status-worsening {
        color: #dc2626;
        font-weight: 700;
    }

    .status-improving {
        color: #16a34a;
        font-weight: 700;
    }

    .status-stable {
        color: #2563eb;
        font-weight: 700;
    }

    .attention-box {
        padding: 1rem;
        border-left: 5px solid #f59e0b;
        background: rgba(245, 158, 11, 0.08);
        border-radius: 8px;
        margin-bottom: 0.8rem;
    }

    .disclaimer-box {
        padding: 1rem;
        border-radius: 10px;
        background: rgba(100, 116, 139, 0.08);
        font-size: 0.9rem;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# Header
# ============================================================

st.title("🏥 Healthcare AI Assistant")

st.markdown(
    """
    <div class="app-subtitle">
        Analyze a health report, compare it with historical
        patient records, and generate AI-assisted health insights.
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# Sidebar
# ============================================================

with st.sidebar:

    st.subheader("About this demo")

    st.info(
        """
        This application uses synthetic medical records
        for demonstration purposes.

        It does not diagnose medical conditions or replace
        advice from a qualified healthcare professional.
        """
    )


# ============================================================
# Upload
# ============================================================

st.subheader("👤 Select Patient")

patient_id = st.selectbox(
    "Patient ID",
    options=[
        "P001",
        "P002",
        "P003",
        "P004",
        "P005",
    ],
    index=None,
    placeholder="Select a patient"
)

st.subheader("📄 Health Report")

uploaded_file = st.file_uploader(
    "Upload a PDF laboratory or health report",
    type=["pdf"],
)


if uploaded_file:

    st.success(
        f"Ready to analyze: {uploaded_file.name}"
    )


analyze_clicked = st.button(
    "🔍 Analyze Health Report",
    type="primary",
    use_container_width=True,
)


# ============================================================
# Run Workflow
# ============================================================

if analyze_clicked:

    if not patient_id:

        st.error(
            "Please select a Patient ID."
        )

    elif uploaded_file is None:

        st.error(
            "Please upload a PDF health report."
        )

    else:

        report_path = None

        try:

            with st.status(
                "Analyzing health report...",
                expanded=True,
            ) as status:

                st.write(
                    "📄 Extracting report content..."
                )

                with tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=".pdf",
                ) as tmp_file:

                    tmp_file.write(
                        uploaded_file.getbuffer()
                    )

                    report_path = tmp_file.name


                report_text = parse_pdf(
                    report_path
                )

                if not report_text.strip():

                    status.update(
                        label="Could not read report",
                        state="error",
                    )

                    st.error(
                        "No text could be extracted "
                        "from this PDF."
                    )

                    st.stop()


                st.write(
                    "🧠 Analyzing current report..."
                )

                st.write(
                    "🔎 Retrieving historical records..."
                )

                st.write(
                    "📈 Comparing health trends..."
                )

                st.write(
                    "💡 Generating recommendations..."
                )


                result = healthcare_graph.invoke(
                    {
                        "patient_id": patient_id,
                        "uploaded_report": report_text,
                        "uploaded_report_path": report_path,
                    }
                )


                st.session_state["result"] = result
                st.session_state["patient_id"] = patient_id

                status.update(
                    label="Analysis completed",
                    state="complete",
                    expanded=False,
                )

        except Exception as error:

            st.error(
                "The healthcare workflow could not "
                "complete successfully."
            )

            with st.expander(
                "Technical error details"
            ):

                st.exception(error)

        finally:

            if (
                report_path
                and os.path.exists(report_path)
            ):
                os.remove(report_path)


# ============================================================
# Results
# ============================================================

if "result" in st.session_state:

    result = st.session_state["result"]

    analysis = result.get(
        "report_analysis",
        {},
    )

    comparison = result.get(
        "comparison_result",
        {},
    )

    recommendations = result.get(
        "recommendations",
        {},
    )


    st.divider()

    # ========================================================
    # Header Summary
    # ========================================================

    st.header("📊 Health Analysis")

    header_col1, header_col2, header_col3 = (
        st.columns(3)
    )

    with header_col1:

        st.metric(
            "Patient",
            st.session_state.get(
                "patient_id",
                "Unknown",
            ),
        )

    with header_col2:

        st.metric(
            "Report Date",
            analysis.get(
                "report_date",
                "Unknown",
            ),
        )

    with header_col3:

        retrieved = result.get(
            "retrieved_documents",
            [],
        )

        st.metric(
            "Historical Records",
            len(retrieved),
        )


    # ========================================================
    # Current Laboratory Values
    # ========================================================

    st.subheader("🧪 Current Laboratory Results")

    lab_values = analysis.get(
        "lab_values",
        [],
    )

    if lab_values:

        columns_per_row = 5

        for start in range(
            0,
            len(lab_values),
            columns_per_row,
        ):

            current_labs = lab_values[
                start:start + columns_per_row
            ]

            cols = st.columns(
                len(current_labs)
            )

            for column, lab in zip(
                cols,
                current_labs,
            ):

                with column:

                    value = lab.get(
                        "value",
                        "N/A",
                    )

                    unit = lab.get(
                        "unit",
                        "",
                    )

                    st.metric(
                        lab.get(
                            "name",
                            "Unknown",
                        ),
                        f"{value} {unit}",
                    )

    else:

        st.info(
            "No laboratory values were extracted."
        )


    # ========================================================
    # Extracted Information
    # ========================================================

    with st.expander(
        "📋 Extracted Report Details"
    ):

        col1, col2 = st.columns(2)

        with col1:

            st.markdown("#### Conditions")

            conditions = analysis.get(
                "conditions",
                [],
            )

            if conditions:
                for item in conditions:
                    st.write(f"• {item}")
            else:
                st.caption(
                    "No conditions were explicitly documented."
                )


            st.markdown("#### Symptoms")

            symptoms = analysis.get(
                "symptoms",
                [],
            )

            if symptoms:
                for item in symptoms:
                    st.write(f"• {item}")
            else:
                st.caption(
                    "No symptoms were explicitly documented."
                )


        with col2:

            st.markdown("#### Medications")

            medications = analysis.get(
                "medications",
                [],
            )

            if medications:
                for item in medications:
                    st.write(f"• {item}")
            else:
                st.caption(
                    "No medications were extracted "
                    "from the current report."
                )


            st.markdown(
                "#### Important Findings"
            )

            important_findings = analysis.get(
                "important_findings",
                [],
            )

            if important_findings:
                for item in important_findings:
                    st.write(f"• {item}")
            else:
                st.caption(
                    "No additional findings were extracted."
                )


    # ========================================================
    # Historical Comparison
    # ========================================================

    st.divider()

    st.header("📈 Historical Comparison")

    comparison_findings = comparison.get(
        "findings",
        [],
    )

    if comparison_findings:

        for finding in comparison_findings:

            parameter = finding.get(
                "parameter",
                "Unknown",
            )

            current_value = finding.get(
                "current_value",
                "N/A",
            )

            historical_value = finding.get(
                "historical_value",
                "N/A",
            )

            trend = finding.get(
                "trend",
                "Unknown",
            )

            explanation = finding.get(
                "explanation",
                "",
            )


            trend_lower = trend.lower()

            if "worsen" in trend_lower:
                icon = "🔴"
                trend_class = (
                    "status-worsening"
                )

            elif "improv" in trend_lower:
                icon = "🟢"
                trend_class = (
                    "status-improving"
                )

            elif "stable" in trend_lower:
                icon = "🔵"
                trend_class = (
                    "status-stable"
                )

            else:
                icon = "⚪"
                trend_class = ""


            with st.container(border=True):

                title_col, trend_col = (
                    st.columns([4, 1])
                )

                with title_col:

                    st.markdown(
                        f"### {parameter}"
                    )

                with trend_col:

                    st.markdown(
                        f"""
                        <span class="{trend_class}">
                            {icon} {trend}
                        </span>
                        """,
                        unsafe_allow_html=True,
                    )


                value_col1, value_col2 = (
                    st.columns(2)
                )

                with value_col1:

                    st.metric(
                        "Current",
                        current_value,
                    )

                with value_col2:

                    st.metric(
                        "Previous",
                        historical_value,
                    )


                if explanation:

                    st.caption(
                        explanation
                    )

    else:

        st.info(
            "No historical comparison was available."
        )


    # ========================================================
    # Overall Trend Summary
    # ========================================================

    overall_summary = comparison.get(
        "overall_summary"
    )

    if overall_summary:

        st.subheader(
            "🧠 Overall Trend"
        )

        st.info(
            overall_summary
        )


    # ========================================================
    # Recommendations
    # ========================================================

    st.divider()

    st.header("💡 Health Guidance")


    if recommendations:

        observations = recommendations.get(
            "observations",
            [],
        )

        discussion_points = recommendations.get(
            "discussion_points",
            [],
        )

        general_guidance = recommendations.get(
            "general_guidance",
            [],
        )

        attention_items = recommendations.get(
            "attention_items",
            [],
        )

        disclaimer = recommendations.get(
            "disclaimer",
            "",
        )


        # ----------------------------------------------------
        # Attention Items
        # ----------------------------------------------------

        if attention_items:

            st.subheader(
                "⚠️ Items to Discuss Promptly"
            )

            for item in attention_items:

                st.markdown(
                    f"""
                    <div class="attention-box">
                        {item}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )


        # ----------------------------------------------------
        # Observations
        # ----------------------------------------------------

        if observations:

            with st.expander(
                "🔎 Key Observations",
                expanded=True,
            ):

                for item in observations:

                    st.write(
                        f"• {item}"
                    )


        # ----------------------------------------------------
        # Discussion Points
        # ----------------------------------------------------

        if discussion_points:

            with st.expander(
                "🩺 Questions to Discuss "
                "with Your Healthcare Provider",
                expanded=True,
            ):

                for item in discussion_points:

                    st.write(
                        f"• {item}"
                    )


        # ----------------------------------------------------
        # General Guidance
        # ----------------------------------------------------

        if general_guidance:

            with st.expander(
                "🌿 General Health Guidance",
                expanded=True,
            ):

                for item in general_guidance:

                    st.write(
                        f"• {item}"
                    )


        # ----------------------------------------------------
        # Disclaimer
        # ----------------------------------------------------

        if disclaimer:

            st.markdown(
                f"""
                <div class="disclaimer-box">
                    <strong>Medical Disclaimer</strong><br><br>
                    {disclaimer}
                </div>
                """,
                unsafe_allow_html=True,
            )

    else:

        st.warning(
            "Recommendations are temporarily unavailable."
        )


    # ========================================================
    # Technical Details
    # ========================================================

    st.divider()

    with st.expander(
        "⚙️ Technical Analysis Details"
    ):

        st.caption(
            "These details are useful for demonstrating "
            "the LangGraph + RAG workflow."
        )

        st.write(
            "**Patient-specific historical records retrieved:**",
            len(
                result.get(
                    "retrieved_documents",
                    [],
                )
            ),
        )

        st.write(
            "**Report date used for historical filtering:**",
            analysis.get(
                "report_date",
                "Unknown",
            ),
        )