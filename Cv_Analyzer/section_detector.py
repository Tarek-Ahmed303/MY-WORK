import re


SECTION_ALIASES = {

    "summary": [
        "summary",
        "professional summary",
        "profile",
        "about me",
        "objective",
        "career objective"
    ],

    "education": [
        "education",
        "academic background",
        "academic qualifications"
    ],

    "experience": [
        "experience",
        "work experience",
        "professional experience",
        "employment history",
        "work history"
    ],

    "skills": [
        "skills",
        "technical skills",
        "core skills",
        "competencies"
    ],

    "projects": [
        "projects",
        "personal projects",
        "academic projects"
    ],

    "certifications": [
        "certifications",
        "certificates",
        "licenses"
    ],

    "languages": [
        "languages",
        "language skills"
    ]
}


def normalize_heading(text):

    text = text.lower().strip()

    text = re.sub(
        r"[^a-zA-Z ]",
        "",
        text
    )

    return text.strip()


def detect_section(line):

    normalized = normalize_heading(line)

    for section, aliases in SECTION_ALIASES.items():

        for alias in aliases:

            if normalized == alias:
                return section

    return None


def split_sections(text):

    sections = {}

    current_section = "header"

    sections[current_section] = []

    for line in text.split("\n"):

        section = detect_section(line)

        if section:

            current_section = section

            sections[current_section] = []

        else:

            sections[current_section].append(line)

    # Convert lists to strings
    for section in sections:

        sections[section] = "\n".join(
            sections[section]
        )

    return sections