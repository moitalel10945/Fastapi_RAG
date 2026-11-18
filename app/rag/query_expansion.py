
import re


# Search terms associated with topics in Morgan's knowledge base.
EXPANSION_RULES = {
    "education": [
        "university", "college", "school", "study", "student",
        "course", "degree", "education", "academic", "enrolled",
        "attend", "graduate"
    ],

    "chuka_university": [
        "chuka", "university", "computer science", "bachelor"
    ],

    "muranga_high_school": [
        "muranga", "high school", "kcse", "secondary school"
    ],

    "professional_experience": [
        "work", "job", "experience", "employment",
        "internship", "attachment", "company", "career"
    ],

    "technical_skills": [
        "programming", "developer", "technology", "framework",
        "language", "software", "technical skills"
    ],

    "personality": [
        "personality", "character", "personal traits",
        "traits", "temperament", "behavior",
        "extroverted", "introverted", "adventurous",
        "easygoing", "independent", "social",
        "problem solving", "working independently"
    ],

    "business": [
        "business", "company", "entrepreneurship",
        "startup", "founder", "resolutetech"
    ],

    "projects": [
        "project", "application", "platform", "software",
        "smartrent", "projectflow"
    ]
}


def expand_query(question: str) -> list[str]:

    normalized_question = re.sub(
        r"[^\w\s]",
        " ",
        question.lower()
    )

    expanded_terms = [question]

    # Prioritise specific education topics.
    if any(term in normalized_question for term in [
        "high school", "secondary school", "kcse", "muranga"
    ]):
        expanded_terms.extend(
            EXPANSION_RULES["muranga_high_school"]
        )

    elif any(term in normalized_question for term in [
        "university", "college", "study", "student",
        "degree", "course", "enrolled", "graduate", "academic"
    ]):
        expanded_terms.extend(EXPANSION_RULES["education"])
        expanded_terms.extend(EXPANSION_RULES["chuka_university"])

    # Other topics.
    for topic in [
        "professional_experience",
        "technical_skills",
        "personality",
        "business",
        "projects"
    ]:
        if any(
            keyword in normalized_question
            for keyword in EXPANSION_RULES[topic]
        ):
            expanded_terms.extend(EXPANSION_RULES[topic])

    return list(dict.fromkeys(expanded_terms))
