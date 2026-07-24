import streamlit as st
import os
import tempfile
from analyzer.document_reader import read_document
from analyzer.nlp_processor import preprocess_text
from analyzer.quality_checker import analyze_srs
from analyzer.explain_ai import explain_prediction
from analyzer.report_generator import generate_pdf_report
# ======================================================
# PAGE CONFIGURATION
# ======================================================
st.set_page_config(
    page_title="SRSentinel AI",
    page_icon="📄",
    layout="wide"
)
# ======================================================
# SIDEBAR
# ======================================================
st.sidebar.title("📄 SRSentinel AI")
st.sidebar.markdown("""
## Intelligent SRS Quality Analyzer
### Features
✅ SRS Document Analysis
✅ NLP Preprocessing
✅ Machine Learning Prediction
✅ Requirement Statistics
✅ Functional Requirement Detection
✅ Non-Functional Requirement Detection
✅ Ambiguity Detection
✅ Explainable AI
✅ Quality Score
✅ PDF Report
---
### Technologies Used
🐍 Python
🧠 Scikit-Learn
📝 NLTK + TF-IDF
🌐 Streamlit
📄 PyPDF2
📑 python-docx
📋 ReportLab
---
### Developed By
**Bhoomi Joshi (24CA1054)**
**Jhanvi Pangam (24CA1053)**
**Aaiman Khan (24CA1061)**
""")
# ======================================================
# MAIN TITLE
# ======================================================
st.title("📄 SRSentinel AI")
st.subheader(
    "Intelligent SRS Quality Analyzer Using NLP and Explainable AI"
)
st.write("""
Upload an IEEE SRS document.
The system will automatically analyze:
- Requirement Quality
- Functional Requirements
- Non-Functional Requirements
- Requirement Statistics
- Ambiguous Words
- Explainable AI Prediction
- Overall Quality Score
""")
# ======================================================
# FILE UPLOAD
# ======================================================
uploaded_file = st.file_uploader(
    "Upload SRS Document",
    type=["pdf", "docx", "txt"]
)
srs_text = st.session_state.get("srs_text", "")
if uploaded_file is not None:
    st.success("✅ File uploaded successfully.")
    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=os.path.splitext(uploaded_file.name)[1]
    ) as temp_file:
        temp_file.write(uploaded_file.getbuffer())
        temp_path = temp_file.name
    srs_text = read_document(temp_path)
    st.session_state["srs_text"] = srs_text
    os.remove(temp_path)
    with st.expander("📄 View Extracted SRS Text"):
        st.text_area(
            "Extracted Text",
            srs_text,
            height=300
        )
        # ======================================================
# ANALYZE BUTTON
# ======================================================
if uploaded_file is not None:
    if st.button(
        "🔍 Analyze SRS Quality",
        use_container_width=True
    ):
        if not srs_text.strip():
            st.error(
                "❌ No text could be extracted from the uploaded document."
            )
        else:
            with st.spinner(
                "Analyzing SRS Document..."
            ):
                # ---------------------------------
                # NLP PREPROCESSING
                # ---------------------------------
                processed_text = preprocess_text(
                    srs_text
                )
                st.session_state[
                    "processed_text"
                ] = processed_text
                # ---------------------------------
                # QUALITY ANALYSIS
                # ---------------------------------
                analysis_result = analyze_srs(
                    processed_text,
                    srs_text
                )
                # ---------------------------------
                # EXPLAINABLE AI
                # ---------------------------------
                explanation = explain_prediction(
                    srs_text
                )
                # ---------------------------------
                # STORE RESULTS
                # ---------------------------------
                st.session_state[
                    "analysis_result"
                ] = analysis_result
                st.session_state[
                    "explanation"
                ] = explanation
            st.success(
                "✅ Analysis completed successfully!"
            )
            # ---------------------------------
            # QUICK SUMMARY
            # ---------------------------------
            prediction = analysis_result.get(
                "prediction",
                "N/A"
            )
            confidence = analysis_result.get(
                "confidence",
                0
            )
            quality_score = analysis_result.get(
                "quality_score",
                0
            )
            st.info(
                f"""
### Analysis Summary
**Prediction:** {prediction}
**Confidence:** {confidence}%
**Quality Score:** {quality_score}/100
"""
            )
            # ======================================================
# DISPLAY ANALYSIS RESULTS
# ======================================================
if "analysis_result" in st.session_state:
    result = st.session_state["analysis_result"]
    st.divider()
    st.header("📊 SRS Quality Analysis Result")
    # --------------------------------------------------
    # METRIC CARDS
    # --------------------------------------------------
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(
            "Prediction",
            result.get("prediction", "N/A")
        )
    with col2:
        st.metric(
            "Confidence",
            f"{result.get('confidence',0)}%"
        )
    with col3:
        st.metric(
            "Quality Score",
            f"{result.get('quality_score',0)}/100"
        )
    # --------------------------------------------------
    # AI ASSESSMENT
    # --------------------------------------------------
    st.subheader("🤖 AI Assessment")
    if result.get("prediction") == "High":
        st.success(
            result.get("message")
        )
    else:
        st.error(
            result.get("message")
        )
    # --------------------------------------------------
    # QUALITY SCORE BAR
    # --------------------------------------------------
    score = result.get("quality_score", 0)
    st.subheader("📈 Overall Quality Score")
    st.progress(score / 100)
    st.write(f"**Overall Score : {score}/100**")
    # ==================================================
    # REQUIREMENT STATISTICS
    # ==================================================
    st.divider()
    st.header("📌 Requirement Statistics")
    statistics = result.get(
        "statistics",
        {}
    )
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(
            "Total Requirements",
            statistics.get(
                "total_requirements",
                0
            )
        )
    with col2:
        st.metric(
            "Functional Requirements",
            statistics.get(
                "functional_requirements",
                0
            )
        )
    with col3:
        st.metric(
            "Non-Functional Requirements",
            statistics.get(
                "non_functional_requirements",
                0
            )
        )
    # ==================================================
    # AMBIGUITY DETECTION
    # ==================================================
    st.divider()
    st.header("⚠️ Ambiguity Detection")
    ambiguous_words = result.get(
        "ambiguous_words",
        []
    )
    if ambiguous_words:
        st.error(
            "Ambiguous Words Found : "
            + ", ".join(ambiguous_words)
        )
    else:
        st.success(
            "No ambiguous words detected ✅"
        )
        # ======================================================
# EXPLAINABLE AI
# ======================================================
if "analysis_result" in st.session_state:
    st.divider()
    st.header("🤖 Explainable AI")
    explanation = st.session_state.get(
        "explanation",
        {}
    )
    st.subheader("Prediction Explanation")
    st.info(
        explanation.get(
            "explanation",
            "No explanation available."
        )
    )
    col1, col2 = st.columns(2)
    # -----------------------------------------
    # Positive Indicators
    # -----------------------------------------
    with col1:
        st.subheader("✅ Positive Indicators")
        positive = explanation.get(
            "positive_features",
            []
        )
        if positive:
            for item in positive:
                st.success(item)
        else:
            st.info(
                "No positive indicators found."
            )
    # -----------------------------------------
    # Negative Indicators
    # -----------------------------------------

    with col2:

        st.subheader("❌ Negative Indicators")

        negative = explanation.get(
            "negative_features",
            []
        )

        if negative:

            for item in negative:

                st.error(item)

        else:

            st.success(
                "No negative indicators found."
            )

    # ======================================================
    # IMPROVEMENT SUGGESTIONS
    # ======================================================

    st.divider()

    st.header("💡 Improvement Suggestions")

    suggestions = st.session_state["analysis_result"].get(
        "suggestions",
        []
    )

    if suggestions:

        for suggestion in suggestions:

            st.write("🔹", suggestion)

    else:

        st.success(
            "Excellent SRS. No improvements required."
        )

    # ======================================================
    # PDF REPORT
    # ======================================================

    st.divider()

    st.header("📄 Generate PDF Report")

    if st.button(
        "Generate PDF Report",
        use_container_width=True
    ):

        with st.spinner(
            "Generating PDF Report..."
        ):

            pdf_path = generate_pdf_report(

                st.session_state["analysis_result"],

                "SRS_Quality_Analysis_Report.pdf"

            )

            st.session_state["pdf_path"] = pdf_path

        st.success(
            "PDF Report Generated Successfully ✅"
        )


# ======================================================
# DOWNLOAD REPORT
# ======================================================

if "pdf_path" in st.session_state:

    pdf_path = st.session_state["pdf_path"]

    if os.path.exists(pdf_path):

        with open(pdf_path, "rb") as pdf:

            st.download_button(

                label="⬇ Download PDF Report",

                data=pdf,

                file_name="SRS_Quality_Analysis_Report.pdf",

                mime="application/pdf",

                use_container_width=True

            )


# ======================================================
# FOOTER
# ======================================================

st.divider()

st.markdown(
    """
    <center>

    <h3>📄 SRSentinel AI</h3>

    <p>
    Intelligent SRS Quality Analyzer Using NLP and Explainable AI
    </p>

    <p>
    Developed By
    </p>

    <b>Bhoomi Joshi (24CA1054)</b><br>
    <b>Jhanvi Pangam (24CA1053)</b><br>
    <b>Aaiman Khan (24CA1061)</b>

    <br><br>

    <i>© 2026 SRSentinel AI | AI-Based Software Requirement Specification Quality Analyzer</i>

    </center>
    """,
    unsafe_allow_html=True
)
