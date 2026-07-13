import streamlit as st
import os
import tempfile


from analyzer.document_reader import read_document

from analyzer.nlp_processor import preprocess_text

from analyzer.quality_checker import analyze_srs

from analyzer.explain_ai import explain_prediction

from analyzer.report_generator import generate_pdf_report



# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(

    page_title=
    "AI SRS Quality Analyzer",

    page_icon="📄",

    layout="wide"

)



# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.title(
    "AI SRS Quality Analyzer"
)


st.sidebar.markdown(
    """
    ### Features

    ✅ SRS Document Analysis

    ✅ NLP Based Processing

    ✅ Machine Learning Prediction

    ✅ Quality Score Generation

    ✅ Requirement Statistics

    ✅ Ambiguity Detection

    ✅ Explainable AI

    ✅ PDF Report Generation


    ---
    
    ### Technologies Used


    🐍 Python

    🧠 Scikit-Learn

    📝 NLP (NLTK + TF-IDF)

    📊 Machine Learning

    🌐 Streamlit

    📄 PyPDF2

    📑 Python-docx

    📋 ReportLab


    ---
    
    ### Developed By

    **BHOOMI JOSHI (24CA1054)**

    **JHANVI PANGAM (24CA1053)**
    
    **AAIMAN KHAN(24CA1061)**

    """
)
# ==========================================
# MAIN PAGE TITLE
# ==========================================

st.title(
    "📄 AI-Based Software Requirement Specification (SRS) Quality Analyzer"
)


st.subheader(
    "Using NLP and Machine Learning for Early Software Defect Prevention"
)


st.write(
    """
    Upload your Software Requirement Specification (SRS) document.
    
    The system will analyze:
    
    - Requirement quality
    - Ambiguous statements
    - Functional and non-functional requirements
    - Overall SRS quality score
    """
)



# ==========================================
# FILE UPLOAD SECTION
# ==========================================

uploaded_file = st.file_uploader(

    "Upload SRS Document",

    type=[
        "txt",
        "pdf",
        "docx"
    ]

)



# Store extracted text

srs_text = st.session_state.get("srs_text", "")



if uploaded_file is not None:


    st.success(
        "File Uploaded Successfully ✅"
    )


    # Create temporary file

    with tempfile.NamedTemporaryFile(

        delete=False,

        suffix=os.path.splitext(
            uploaded_file.name
        )[1]

    ) as temp_file:


        temp_file.write(

            uploaded_file.getbuffer()

        )


        temp_path = temp_file.name




    # Read document

    srs_text = read_document(

        temp_path

    )
    st.session_state["srs_text"] = srs_text



    # Delete temporary file

    os.remove(
        temp_path
    )



    # Display extracted text

    with st.expander(
        "View Extracted SRS Text"
    ):


        st.text_area(

            "Extracted Content",

            srs_text,

            height=250

        )
        # ==========================================
# ANALYZE BUTTON
# ==========================================

if uploaded_file is not None:


    if st.button(
        "🔍 Analyze SRS Quality"
    ):


        if srs_text.strip() == "":


            st.error(
                "No text found in document."
            )


        else:


            with st.spinner(
                "Analyzing SRS using AI Model..."
            ):



                # NLP preprocessing

                processed_text = preprocess_text(

                    srs_text

                )



                # Quality prediction

                analysis_result = analyze_srs(

                    processed_text

                )



                # Save result

                st.session_state[
                    "analysis_result"
                ] = analysis_result



            st.success(
                "Analysis Completed Successfully ✅"
            )



# ==========================================
# DISPLAY RESULTS
# ==========================================


if "analysis_result" in st.session_state:


    result = st.session_state[
        "analysis_result"
    ]



    st.divider()



    st.header(
        "📊 SRS Quality Analysis Result"
    )



    # ------------------------------
    # Prediction Cards
    # ------------------------------


    col1, col2, col3 = st.columns(3)



    with col1:


        st.metric(

            "Prediction",

            result.get(
                "prediction",
                "N/A"
            )

        )



    with col2:


        st.metric(

            "Confidence",

            str(
                result.get(
                    "confidence",
                    0
                )
            )
            + "%"

        )



    with col3:


        st.metric(

            "Quality Score",

            str(
                result.get(
                    "quality_score",
                    0
                )
            )
            + "/100"

        )




    # ------------------------------
    # Quality Message
    # ------------------------------


    st.subheader(
        "AI Assessment"
    )


    st.info(

        result.get(

            "message",

            "No message available"

        )

    )
    # ==========================================
# REQUIREMENT STATISTICS
# ==========================================

if "analysis_result" in st.session_state:


    result = st.session_state[
        "analysis_result"
    ]



    st.divider()



    st.header(
        "📌 Requirement Statistics"
    )



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





    # ==========================================
    # AMBIGUITY DETECTION
    # ==========================================


    st.divider()


    st.header(
        "⚠️ Ambiguity Detection"
    )



    ambiguous_words = result.get(

        "ambiguous_words",

        []

    )



    if ambiguous_words:


        st.warning(

            "Ambiguous words detected: "

            +

            ", ".join(
                ambiguous_words
            )

        )


    else:


        st.success(

            "No ambiguous words detected ✅"

        )




# ==========================================
# EXPLAINABLE AI
# ==========================================

st.divider()

st.header("🤖 Explainable AI Analysis")

if "analysis_result" in st.session_state:

    if srs_text.strip():

        processed_text = preprocess_text(srs_text)
        st.session_state["processed_text"] = processed_text
         
        explanation = explain_prediction(processed_text)

        st.subheader("Prediction Reason")

        st.info(
            explanation.get(
                "explanation",
                "No explanation available"
            )
        )

        col1, col2 = st.columns(2)

        with col1:

            st.subheader("✅ Positive Indicators")

            positive = explanation.get(
                "positive_features",
                []
            )

            if positive:

                for word in positive:
                    st.write("✔", word)

            else:

                st.write("No positive indicators found")

        with col2:

            st.subheader("❌ Negative Indicators")

            negative = explanation.get(
                "negative_features",
                []
            )

            if negative:

                for word in negative:
                    st.write("⚠", word)

            else:

                st.write("No negative indicators found")
   

    # ==========================================
    # IMPROVEMENT SUGGESTIONS
    # ==========================================


    st.divider()


    st.header(
        "💡 Improvement Suggestions"
    )



    suggestions = result.get(

        "suggestions",

        []

    )



    if suggestions:


        for suggestion in suggestions:


            st.write(

                "🔹",

                suggestion

            )


    else:


        st.success(

            "Your SRS follows good quality practices."

        )
        # ==========================================
# PDF REPORT GENERATION
# ==========================================

if "analysis_result" in st.session_state:


    result = st.session_state[
        "analysis_result"
    ]



    st.divider()



    st.header(
        "📄 Generate SRS Analysis Report"
    )



    if st.button(
        "Generate PDF Report"
    ):


        with st.spinner(
            "Creating PDF Report..."
        ):


            pdf_path = generate_pdf_report(

                result,

                "SRS_Quality_Analysis_Report.pdf"

            )


            st.session_state[
                "pdf_path"
            ] = pdf_path



        st.success(

            "PDF Report Generated Successfully ✅"

        )





# ==========================================
# DOWNLOAD PDF
# ==========================================

if "pdf_path" in st.session_state:


    pdf_file = st.session_state[
        "pdf_path"
    ]



    if os.path.exists(pdf_file):


        with open(
            pdf_file,
            "rb"
        ) as file:


            st.download_button(

                label=
                "⬇️ Download PDF Report",

                data=file,

                file_name=
                "SRS_Quality_Analysis_Report.pdf",

                mime=
                "application/pdf"

            )





# ==========================================
# FOOTER
# ==========================================


st.divider()


st.markdown(

    """
    <center>

    <h4>
    AI-Based Software Requirement Specification 
    (SRS) Quality Analyzer
    </h4>

    <br>


    </center>

    """,

    unsafe_allow_html=True

)