import os

from reportlab.lib.styles import getSampleStyleSheet

from reportlab.platypus import (

    SimpleDocTemplate,

    Paragraph,

    Spacer

)
# =====================================================
# PDF REPORT
# =====================================================

def generate_pdf_report(

        result,

        output_path

):

    doc = SimpleDocTemplate(

        output_path

    )

    styles = getSampleStyleSheet()

    story = []

    # ----------------------------------------

    story.append(

        Paragraph(

            "<b>SRSentinel AI</b>",

            styles["Title"]

        )

    )

    story.append(

        Paragraph(

            "Software Requirement Specification Analysis Report",

            styles["Heading2"]

        )

    )

    story.append(

        Spacer(1, 20)

    )
        # ========================================

    story.append(

        Paragraph(

            "<b>Prediction :</b> " +

            str(result.get("prediction", "N/A")),

            styles["Normal"]

        )

    )

    story.append(

        Paragraph(

            "<b>Confidence :</b> "

            + str(result.get("confidence", 0))

            + "%",

            styles["Normal"]

        )

    )

    story.append(

        Paragraph(

            "<b>Quality Score :</b> "

            + str(result.get("quality_score", 0))

            + "/100",

            styles["Normal"]

        )

    )

    story.append(

        Paragraph(

            "<b>Assessment :</b> "

            + result.get("message", ""),

            styles["Normal"]

        )

    )

    story.append(

        Spacer(1, 15)

    )
        # ========================================
    # Requirement Statistics
    # ========================================

    statistics = result.get("statistics", {})

    story.append(

        Paragraph(

            "<b>Requirement Statistics</b>",

            styles["Heading2"]

        )

    )

    story.append(

        Paragraph(

            "Total Requirements : "

            + str(statistics.get("total_requirements", 0)),

            styles["Normal"]

        )

    )

    story.append(

        Paragraph(

            "Functional Requirements : "

            + str(statistics.get("functional_requirements", 0)),

            styles["Normal"]

        )

    )

    story.append(

        Paragraph(

            "Non-Functional Requirements : "

            + str(statistics.get("non_functional_requirements", 0)),

            styles["Normal"]

        )

    )

    story.append(

        Spacer(1, 15)

    )
        # ========================================
    # Ambiguous Words
    # ========================================

    story.append(

        Paragraph(

            "<b>Ambiguous Words</b>",

            styles["Heading2"]

        )

    )

    ambiguity = result.get(

        "ambiguous_words",

        []

    )

    if ambiguity:

        story.append(

            Paragraph(

                ", ".join(ambiguity),

                styles["Normal"]

            )

        )

    else:

        story.append(

            Paragraph(

                "No ambiguous words detected.",

                styles["Normal"]

            )

        )

    story.append(

        Spacer(1, 15)

    )
        # ========================================
    # Suggestions
    # ========================================

    story.append(

        Paragraph(

            "<b>Improvement Suggestions</b>",

            styles["Heading2"]

        )

    )

    suggestions = result.get(

        "suggestions",

        []

    )

    if suggestions:

        for suggestion in suggestions:

            story.append(

                Paragraph(

                    "• " + suggestion,

                    styles["Normal"]

                )

            )

    else:

        story.append(

            Paragraph(

                "No improvements required.",

                styles["Normal"]

            )

        )

    # ========================================

    doc.build(story)

    return output_path
