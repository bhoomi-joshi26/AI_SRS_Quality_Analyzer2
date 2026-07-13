from analyzer.report_generator import generate_pdf_report



sample_result = {


"prediction":"High",

"confidence":95,

"quality_score":90,


"statistics":
{
"total_requirements":10,
"functional_requirements":7,
"non_functional_requirements":3
},


"ambiguous_words":[],

"message":
"The SRS contains clear and measurable requirements.",


"suggestions":[]

}



path = generate_pdf_report(
    sample_result,
    "test_report.pdf"
)



print(
    "PDF Created:",
    path
)