import os

from reportlab.lib.pagesizes import letter

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet




# =========================================
# REPORT FOLDER
# =========================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


REPORT_FOLDER = os.path.join(
    BASE_DIR,
    "reports"
)



if not os.path.exists(REPORT_FOLDER):

    os.makedirs(
        REPORT_FOLDER
    )





# =========================================
# PDF GENERATOR FUNCTION
# =========================================

def generate_pdf_report(
        analysis_result,
        file_name="SRS_Report.pdf"
):


    report_path = os.path.join(

        REPORT_FOLDER,

        file_name

    )



    document = SimpleDocTemplate(

        report_path,

        pagesize=letter

    )



    styles = getSampleStyleSheet()


    content = []



    # -------------------------------
    # Title
    # -------------------------------

    title = Paragraph(

        "<b>AI-Based Software Requirement "
        "Specification (SRS) Quality Analyzer</b>",

        styles["Title"]

    )


    content.append(title)

    content.append(
        Spacer(1,20)
    )





    # -------------------------------
    # Prediction Details
    # -------------------------------


    content.append(

        Paragraph(

            "<b>Prediction:</b> "
            + str(
                analysis_result.get(
                    "prediction"
                )
            ),

            styles["Normal"]

        )

    )



    content.append(

        Paragraph(

            "<b>Confidence:</b> "
            + str(
                analysis_result.get(
                    "confidence"
                )
            )
            + "%",

            styles["Normal"]

        )

    )



    content.append(

        Paragraph(

            "<b>Quality Score:</b> "
            + str(
                analysis_result.get(
                    "quality_score"
                )
            )
            + "/100",

            styles["Normal"]

        )

    )



    content.append(
        Spacer(1,15)
    )




    # -------------------------------
    # Statistics
    # -------------------------------


    content.append(

        Paragraph(

            "<b>Requirement Statistics</b>",

            styles["Heading2"]

        )

    )



    statistics = analysis_result.get(
        "statistics",
        {}
    )


    for key,value in statistics.items():


        content.append(

            Paragraph(

                f"{key}: {value}",

                styles["Normal"]

            )

        )




    content.append(
        Spacer(1,15)
    )




    # -------------------------------
    # Ambiguity Detection
    # -------------------------------


    content.append(

        Paragraph(

            "<b>Ambiguous Words Detected</b>",

            styles["Heading2"]

        )

    )



    ambiguous = analysis_result.get(

        "ambiguous_words",

        []

    )



    if ambiguous:


        content.append(

            Paragraph(

                ", ".join(ambiguous),

                styles["Normal"]

            )

        )


    else:


        content.append(

            Paragraph(

                "No ambiguous words detected",

                styles["Normal"]

            )

        )





    content.append(
        Spacer(1,15)
    )





    # -------------------------------
    # Explanation
    # -------------------------------


    content.append(

        Paragraph(

            "<b>AI Explanation</b>",

            styles["Heading2"]

        )

    )



    content.append(

        Paragraph(

            analysis_result.get(

                "message",

                analysis_result.get(
                    "explanation",
                    ""
                )

            ),

            styles["Normal"]

        )

    )





    content.append(
        Spacer(1,15)
    )





    # -------------------------------
    # Suggestions
    # -------------------------------


    content.append(

        Paragraph(

            "<b>Improvement Suggestions</b>",

            styles["Heading2"]

        )

    )



    suggestions = analysis_result.get(

        "suggestions",

        []

    )



    if suggestions:


        for item in suggestions:


            content.append(

                Paragraph(

                    "• " + item,

                    styles["Normal"]

                )

            )


    else:


        content.append(

            Paragraph(

                "No major improvements required.",

                styles["Normal"]

            )

        )





    # Build PDF

    document.build(
        content
    )


    return report_path