# Self reasoning agent templates
READ_JSON_TEMPLATE = dict(
    template=(
        "You are an AI helping in cleaning the json input containing the HTML, "
        "obtained by scraping a linkedin profile. You must extract "
        "the information related to the career of the person and ignore all "
        "other information.\n"
        "Here is the json file:\n{website}\n"
        "Now provide the information related to the career of the person:\n"
    ),
    input_variables=["website"],
)

READ_CURRICULUM_TEMPLATE = dict(
    template=(
        "You are an AI helping in summarizing the curriculum of a person. "
        "You must extract the information related to the career of the person "
        "and ignore all other information.\n"
        "Here is the curriculum:\n{curriculum}\n"
        "Now provide the information related to the career of the person:\n"
    ),
    input_variables=["curriculum"],
)

GENERATE_BIO_TEMPLATE = dict(
    template=(
        "You are an AI helping in generating a bio for a person. The bio "
        "must be a short description of the person's career. Consider that "
        "the bio will be used in the application process for participating"
        "to a conference.\n"
        "Thw bio must be a short, but at the same time complete and it must "
        "highlight the most important aspects of the person's career.\n"
        "Here is the curriculum:\n{curriculum}\n"
        "And here is the linkedin profile:\n{website}\n"
        "Now provide the bio for the person:\n"
    ),
    input_variables=["curriculum", "website"],
)