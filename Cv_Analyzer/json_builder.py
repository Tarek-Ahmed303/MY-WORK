import re
from datetime import datetime


# ============================================================
# HELPERS
# ============================================================

def get_section(sections, name):
    """
    Safely get a section from the detected CV sections.
    """
    return sections.get(name, "").strip()


def split_lines(text):
    """
    Convert section text into clean non-empty lines.
    """
    return [
        line.strip()
        for line in text.split("\n")
        if line.strip()
    ]


def extract_bullets(text):
    """
    Extract bullet-point descriptions.
    """
    bullets = []

    for line in split_lines(text):
        line = re.sub(r"^[•●▪◦\-*]\s*", "", line).strip()

        if line:
            bullets.append(line)

    return bullets


def unique(items):
    """
    Remove duplicates while preserving order.
    """
    result = []

    for item in items:
        if item and item not in result:
            result.append(item)

    return result


# ============================================================
# EDUCATION
# ============================================================

def parse_education(text):
    if not text:
        return []

    lines = split_lines(text)
    lines = [line.strip() for line in lines if line.strip()]

    education = []

    def is_year(line):
        return bool(re.fullmatch(r"\d{4}", line.strip()))

    def extract_date_range(line):
        match = re.search(
            r"(\d{1,2}/\d{4}|\d{4})"
            r"\s*[-–—]\s*"
            r"(\d{1,2}/\d{4}|\d{4}|Present)",
            line,
            re.IGNORECASE
        )

        if match:
            return match.group(1), match.group(2)

        return None, None

    def looks_like_institution(line):
        return bool(re.search(
            r"\b(university|college|institute|school|academy)\b",
            line,
            re.IGNORECASE
        ))

    def extract_degree(line):
        match = re.search(
            r"\b("
            r"Bachelor(?:'s)?|Master(?:'s)?|PhD|Doctorate|"
            r"B\.?Sc\.?|M\.?Sc\.?|B\.?A\.?|M\.?A\.?"
            r")\b",
            line,
            re.IGNORECASE
        )

        if not match:
            return None, None

        degree = match.group(1)

        field = None

        field_match = re.search(
            r"(?:in|of)\s+(.+)",
            line,
            re.IGNORECASE
        )

        if field_match:
            field = field_match.group(1).strip()

        return degree, field

    def add_education(start, end, nearby):
        institution = None
        degree = None
        field = None

        for line in nearby:
            d, f = extract_degree(line)

            if d and degree is None:
                degree = d

            if f and field is None:
                field = f

            if looks_like_institution(line) and institution is None:
                institution = line

        # If institution has a location after |
        if institution and "|" in institution:
            institution = institution.split("|")[0].strip()

        if institution or degree:
            education.append({
                "degree": degree,
                "institution": institution,
                "field": field,
                "start_date": start,
                "end_date": end,
                "gpa": None
            })

    i = 0

    while i < len(lines):

        # --------------------------------------------------
        # FORMAT:
        # 2017 - 2021
        # University
        # Bachelor of Computer Science
        # --------------------------------------------------

        start, end = extract_date_range(lines[i])

        if start:
            nearby = []
            j = i + 1

            while j < len(lines):

                # A new date range means a new education entry
                if extract_date_range(lines[j])[0]:
                    break

                # Two consecutive years means a new entry
                if (
                    is_year(lines[j])
                    and j + 1 < len(lines)
                    and is_year(lines[j + 1])
                ):
                    break

                nearby.append(lines[j])
                j += 1

            add_education(start, end, nearby)

            i = j
            continue

        # --------------------------------------------------
        # FORMAT:
        # 2017
        # 2021
        # University
        # Bachelor ...
        # --------------------------------------------------

        if (
            is_year(lines[i])
            and i + 1 < len(lines)
            and is_year(lines[i + 1])
        ):
            start = lines[i]
            end = lines[i + 1]

            nearby = []
            j = i + 2

            while j < len(lines):

                if extract_date_range(lines[j])[0]:
                    break

                if (
                    is_year(lines[j])
                    and j + 1 < len(lines)
                    and is_year(lines[j + 1])
                ):
                    break

                nearby.append(lines[j])
                j += 1

            add_education(start, end, nearby)

            i = j
            continue

        # --------------------------------------------------
        # FORMAT:
        # University
        # Bachelor ...
        # 2017 - 2021
        # --------------------------------------------------

        if looks_like_institution(lines[i]):

            institution = lines[i]

            if "|" in institution:
                institution = institution.split("|")[0].strip()

            degree = None
            field = None
            start = None
            end = None

            j = i + 1

            while j < len(lines):

                # Stop when next education starts
                if (
                    is_year(lines[j])
                    and j + 1 < len(lines)
                    and is_year(lines[j + 1])
                ):
                    break

                d1, d2 = extract_date_range(lines[j])

                if d1:
                    start = d1
                    end = d2
                    j += 1
                    break

                d, f = extract_degree(lines[j])

                if d:
                    degree = d

                if f:
                    field = f

                j += 1

            # Handle separate years
            if (
                start is None
                and j + 1 < len(lines)
                and is_year(lines[j])
                and is_year(lines[j + 1])
            ):
                start = lines[j]
                end = lines[j + 1]
                j += 2

            if institution or degree:
                education.append({
                    "degree": degree,
                    "institution": institution,
                    "field": field,
                    "start_date": start,
                    "end_date": end,
                    "gpa": None
                })

            i = j
            continue

        i += 1

    return education
# ============================================================
# EXPERIENCE
# ============================================================

def parse_experience(text):
    if not text:
        return []

    lines = split_lines(text)
    lines = [line.strip() for line in lines if line.strip()]

    experiences = []

    def is_year(line):
        return bool(re.fullmatch(r"\d{4}", line.strip()))

    def extract_date_range(line):
        match = re.search(
            r"(\d{1,2}/\d{4}|\d{4})"
            r"\s*[-–—]\s*"
            r"(\d{1,2}/\d{4}|\d{4}|Present)",
            line,
            re.IGNORECASE
        )

        if match:
            return match.group(1), match.group(2)

        return None, None

    def looks_like_job_heading(line):
        """
        Detect lines such as:

        Data Engineering Track – DEPI | 08/2026 – Present
        AI & Machine Learning Trainee – ITI | 07/2026 – 08/2026
        Software Engineer - Google
        """

        # Must contain a separator between job title and company
        if not re.search(r"\s[-–—]\s", line):
            return False

        # Ignore lines that are only date ranges
        if extract_date_range(line)[0]:
            return True

        return True

    def extract_job_heading(line):
        """
        Extract job title and company from:

        Data Engineering Track – DEPI | 08/2026 – Present
        AI & Machine Learning Trainee – ITI | 07/2026 – 08/2026
        """

        # Remove date part
        cleaned = re.sub(
            r"\s*\|\s*"
            r"\d{1,2}/\d{4}\s*[-–—]\s*"
            r"(?:\d{1,2}/\d{4}|\d{4}|Present)"
            r"\s*$",
            "",
            line,
            flags=re.IGNORECASE
        ).strip()

        # Also handle date without |
        cleaned = re.sub(
            r"\s+"
            r"\d{1,2}/\d{4}\s*[-–—]\s*"
            r"(?:\d{1,2}/\d{4}|\d{4}|Present)"
            r"\s*$",
            "",
            cleaned,
            flags=re.IGNORECASE
        ).strip()

        # Split title and company
        match = re.match(
            r"^(.+?)\s+[-–—]\s+(.+)$",
            cleaned
        )

        if match:
            job_title = match.group(1).strip()
            company = match.group(2).strip()

            return job_title, company

        return None, None

    def add_experience(
        job_title,
        company,
        start,
        end,
        description
    ):
        if job_title or company:
            experiences.append({
                "job_title": job_title,
                "company": company,
                "location": None,
                "start_date": start,
                "end_date": end,
                "description": description,
                "technologies": []
            })

    i = 0

    while i < len(lines):

        # --------------------------------------------------
        # FORMAT:
        #
        # Data Engineering Track – DEPI | 08/2026 – Present
        # • Description
        # • Description
        # --------------------------------------------------

        if looks_like_job_heading(lines[i]):

            job_title, company = extract_job_heading(lines[i])

            if job_title or company:

                start, end = extract_date_range(lines[i])

                description = []

                j = i + 1

                while j < len(lines):

                    # A new job heading means a new experience
                    if looks_like_job_heading(lines[j]):
                        break

                    # A new date range by itself means a new entry
                    if extract_date_range(lines[j])[0]:
                        break

                    # Separate year format
                    if (
                        is_year(lines[j])
                        and j + 1 < len(lines)
                        and is_year(lines[j + 1])
                    ):
                        break

                    # Remove bullet symbol
                    bullet = re.sub(
                        r"^[•●▪◦\-*]\s*",
                        "",
                        lines[j]
                    ).strip()

                    if bullet:
                        description.append(bullet)

                    j += 1

                # --------------------------------------------------
                # If dates are on the next line
                #
                # Data Engineering Track – DEPI
                # 08/2026 – Present
                # --------------------------------------------------

                if start is None:

                    if j < len(lines):
                        d1, d2 = extract_date_range(lines[j])

                        if d1:
                            start = d1
                            end = d2
                            j += 1

                # --------------------------------------------------
                # Separate years
                #
                # Data Engineering Track – DEPI
                # 2026
                # 2027
                # --------------------------------------------------

                if (
                    start is None
                    and j + 1 < len(lines)
                    and is_year(lines[j])
                    and is_year(lines[j + 1])
                ):
                    start = lines[j]
                    end = lines[j + 1]
                    j += 2

                add_experience(
                    job_title,
                    company,
                    start,
                    end,
                    description
                )

                i = j
                continue

        # --------------------------------------------------
        # FORMAT:
        #
        # 08/2026 – Present
        # Data Engineering Track – DEPI
        # • Description
        # --------------------------------------------------

        start, end = extract_date_range(lines[i])

        if start:

            nearby = []
            j = i + 1

            while j < len(lines):

                if looks_like_job_heading(lines[j]):
                    break

                if extract_date_range(lines[j])[0]:
                    break

                nearby.append(lines[j])
                j += 1

            job_title = None
            company = None
            description = []

            for line in nearby:

                title, comp = extract_job_heading(line)

                if title or comp:
                    if job_title is None:
                        job_title = title

                    if company is None:
                        company = comp

                else:
                    bullet = re.sub(
                        r"^[•●▪◦\-*]\s*",
                        "",
                        line
                    ).strip()

                    if bullet:
                        description.append(bullet)

            add_experience(
                job_title,
                company,
                start,
                end,
                description
            )

            i = j
            continue

        # --------------------------------------------------
        # FORMAT:
        #
        # Data Engineering Track – DEPI
        # 08/2026 – Present
        # • Description
        # --------------------------------------------------

        if looks_like_job_heading(lines[i]):

            job_title, company = extract_job_heading(lines[i])

            start = None
            end = None
            description = []

            j = i + 1

            while j < len(lines):

                d1, d2 = extract_date_range(lines[j])

                if d1:
                    start = d1
                    end = d2
                    j += 1
                    break

                if (
                    is_year(lines[j])
                    and j + 1 < len(lines)
                    and is_year(lines[j + 1])
                ):
                    start = lines[j]
                    end = lines[j + 1]
                    j += 2
                    break

                bullet = re.sub(
                    r"^[•●▪◦\-*]\s*",
                    "",
                    lines[j]
                ).strip()

                if bullet:
                    description.append(bullet)

                j += 1

            # Collect remaining description
            while j < len(lines):

                if looks_like_job_heading(lines[j]):
                    break

                if extract_date_range(lines[j])[0]:
                    break

                if (
                    is_year(lines[j])
                    and j + 1 < len(lines)
                    and is_year(lines[j + 1])
                ):
                    break

                bullet = re.sub(
                    r"^[•●▪◦\-*]\s*",
                    "",
                    lines[j]
                ).strip()

                if bullet:
                    description.append(bullet)

                j += 1

            add_experience(
                job_title,
                company,
                start,
                end,
                description
            )

            i = j
            continue

        i += 1

    return experiences
# ============================================================
# SKILLS
# ============================================================

def parse_skills(text):
    if not text:
        return {
            "technical": [],
            "soft": []
        }

    technical = []
    soft = []

    # --------------------------------------------------------
    # Known technical skills
    # --------------------------------------------------------

    technical_keywords = [
        "Python",
        "SQL",
        "C++",
        "Machine Learning",
        "Deep Learning",
        "Supervised Learning",
        "Unsupervised Learning",
        "Feature Engineering",
        "Data Preprocessing",
        "ETL Pipelines",
        "Git",
        "GitHub",
        "Jupyter Notebook",
        "Pandas",
        "NumPy",
        "Scikit-Learn",
        "Matplotlib",
        "Seaborn",
        "Power BI",
        "TensorFlow",
        "PyTorch",
        "NLP",
        "Computer Vision",
        "Data Analysis",
        "Database Design"
    ]

    for skill in technical_keywords:

        if re.search(
            r"\b" + re.escape(skill) + r"\b",
            text,
            re.IGNORECASE
        ):
            technical.append(skill)

    # --------------------------------------------------------
    # Soft skills
    # --------------------------------------------------------

    soft_keywords = [
        "Communication",
        "Leadership",
        "Teamwork",
        "Problem Solving",
        "Critical Thinking",
        "Time Management",
        "Adaptability",
        "Creativity"
    ]

    for skill in soft_keywords:

        if re.search(
            r"\b" + re.escape(skill) + r"\b",
            text,
            re.IGNORECASE
        ):
            soft.append(skill)

    return {
        "technical": unique(technical),
        "soft": unique(soft)
    }


# ============================================================
# PROJECTS
# ============================================================

def parse_projects(text):
    if not text:
        return []

    lines = split_lines(text)

    projects = []

    current_project = None

    for line in lines:

        # ----------------------------------------------------
        # Detect project heading
        # ----------------------------------------------------

        # Example:
        # Car Price Prediction | Python, Scikit-Learn, NumPy | 2026

        if "|" in line and not line.startswith(("•", "-", "*")):

            parts = [
                p.strip()
                for p in line.split("|")
            ]

            if len(parts) >= 2:

                # Save previous project
                if current_project:
                    projects.append(current_project)

                name = parts[0]

                technologies = []

                if len(parts) >= 2:

                    technologies = [
                        x.strip()
                        for x in parts[1].split(",")
                        if x.strip()
                    ]

                current_project = {
                    "name": name,
                    "description": [],
                    "technologies": technologies,
                    "url": None
                }

                continue

        # ----------------------------------------------------
        # Project description
        # ----------------------------------------------------

        if current_project:

            line = re.sub(
                r"^[•●▪◦\-*]\s*",
                "",
                line
            )

            current_project["description"].append(line)

    # Save final project
    if current_project:
        projects.append(current_project)

    return projects


# ============================================================
# CERTIFICATIONS
# ============================================================

def parse_certifications(text):
    if not text:
        return []

    lines = split_lines(text)

    certifications = []

    for line in lines:

        line = re.sub(
            r"^[•●▪◦\-*]\s*",
            "",
            line
        )

        if line:

            certifications.append({
                "name": line,
                "issuer": None,
                "date": None
            })

    return certifications


# ============================================================
# LANGUAGES
# ============================================================

def parse_languages(text):
    if not text:
        return []

    languages = []

    # Known languages
    known_languages = [
        "Arabic",
        "English",
        "French",
        "German",
        "Spanish",
        "Italian",
        "Chinese",
        "Japanese"
    ]

    for language in known_languages:

        if re.search(
            r"\b" + language + r"\b",
            text,
            re.IGNORECASE
        ):

            languages.append({
                "language": language,
                "proficiency": None
            })

    return languages


# ============================================================
# CAREER
# ============================================================

def calculate_years_of_experience(experiences):

    if not experiences:
        return 0

    current_year = datetime.now().year

    years = []

    for exp in experiences:

        start = exp.get("start_date")

        if not start:
            continue

        match = re.search(r"(\d{4})", start)

        if not match:
            continue

        start_year = int(match.group(1))

        end = exp.get("end_date")

        if end and "present" not in end.lower():

            end_match = re.search(r"(\d{4})", end)

            if end_match:
                end_year = int(end_match.group(1))
            else:
                end_year = current_year

        else:
            end_year = current_year

        if end_year >= start_year:
            years.append(end_year - start_year)

    if not years:
        return 0

    return max(years)


# ============================================================
# INTERVIEW CONTEXT
# ============================================================

def build_interview_context(
    projects,
    experiences,
    skills
):

    project_names = [
        project["name"]
        for project in projects
        if project.get("name")
    ]

    technologies = skills["technical"].copy()

    for project in projects:

        for tech in project.get("technologies", []):

            if tech not in technologies:
                technologies.append(tech)

    experience_topics = []

    for experience in experiences:

        title = experience.get("job_title")

        if title:
            experience_topics.append(title)

        for description in experience.get("description", []):

            # Keep important technical topics
            for keyword in [
                "Python",
                "SQL",
                "Machine Learning",
                "Data Engineering",
                "ETL",
                "Data Analysis",
                "Feature Engineering",
                "Database",
                "Deep Learning"
            ]:

                if re.search(
                    r"\b" + re.escape(keyword) + r"\b",
                    description,
                    re.IGNORECASE
                ):

                    if keyword not in experience_topics:
                        experience_topics.append(keyword)

    return {
        "projects": project_names,
        "technologies": unique(technologies),
        "experience_topics": unique(experience_topics),
        "claims_to_verify": []
    }


# ============================================================
# QUALITY
# ============================================================

def calculate_quality(
    text,
    sections,
    contact,
    education,
    experience,
    skills,
    projects,
    languages
):

    completeness_points = 0
    total_points = 8

    if contact.get("email"):
        completeness_points += 1

    if contact.get("phone"):
        completeness_points += 1

    if get_section(sections, "summary"):
        completeness_points += 1

    if education:
        completeness_points += 1

    if experience:
        completeness_points += 1

    if skills["technical"]:
        completeness_points += 1

    if projects:
        completeness_points += 1

    if languages:
        completeness_points += 1

    completeness = round(
        completeness_points / total_points * 100
    )

    # Basic readability score
    readability = 90

    if len(text) < 500:
        readability = 70

    # Structure score
    detected_sections = sum(
        1
        for key, value in sections.items()
        if key != "header" and value
    )

    structure = min(
        100,
        detected_sections * 15
    )

    formatting_issues = []

    if not contact.get("email"):
        formatting_issues.append("Email not detected")

    if not contact.get("phone"):
        formatting_issues.append("Phone not detected")

    return {
        "completeness": completeness,
        "readability": readability,
        "structure": structure,
        "formatting_issues": formatting_issues
    }


# ============================================================
# MAIN JSON BUILDER
# ============================================================

def build_resume(
    resume_id,
    sections,
    contact,
    entities
):

    # --------------------------------------------------------
    # NAME
    # --------------------------------------------------------

    name = None

    for entity in entities:

        if entity["label"] == "PERSON":
            name = entity["text"]
            break

    # --------------------------------------------------------
    # LOCATION
    # --------------------------------------------------------

    location = None

    for entity in entities:

        if entity["label"] in ["GPE", "LOC"]:

            location = entity["text"]
            break

    # --------------------------------------------------------
    # SECTIONS
    # --------------------------------------------------------

    summary = get_section(
        sections,
        "summary"
    )

    education_text = get_section(
        sections,
        "education"
    )

    experience_text = get_section(
        sections,
        "experience"
    )

    skills_text = get_section(
        sections,
        "skills"
    )

    projects_text = get_section(
        sections,
        "projects"
    )

    certifications_text = get_section(
        sections,
        "certifications"
    )

    languages_text = get_section(
        sections,
        "languages"
    )

    # --------------------------------------------------------
    # PARSE EACH SECTION
    # --------------------------------------------------------

    education = parse_education(
        education_text
    )

    experience = parse_experience(
        experience_text
    )

    skills = parse_skills(
        skills_text
    )

    projects = parse_projects(
        projects_text
    )

    certifications = parse_certifications(
        certifications_text
    )

    languages = parse_languages(
        languages_text
    )

    # --------------------------------------------------------
    # CAREER
    # --------------------------------------------------------

    job_titles = unique([
        exp["job_title"]
        for exp in experience
        if exp.get("job_title")
    ])

    years_of_experience = calculate_years_of_experience(
        experience
    )

    career = {
        "job_titles": job_titles,
        "years_of_experience": years_of_experience
    }

    # --------------------------------------------------------
    # INTERVIEW CONTEXT
    # --------------------------------------------------------

    interview_context = build_interview_context(
        projects,
        experience,
        skills
    )

    # --------------------------------------------------------
    # QUALITY
    # --------------------------------------------------------

    quality = calculate_quality(
        text=summary + "\n" + education_text +
             "\n" + experience_text +
             "\n" + skills_text +
             "\n" + projects_text,

        sections=sections,
        contact=contact,
        education=education,
        experience=experience,
        skills=skills,
        projects=projects,
        languages=languages
    )

    # --------------------------------------------------------
    # FINAL JSON
    # --------------------------------------------------------

    return {
        "resume_id": resume_id,

        "candidate": {
            "name": name,
            "email": contact.get("email"),
            "phone": contact.get("phone"),
            "location": location,
            "linkedin": contact.get("linkedin"),
            "github": contact.get("github"),
            "portfolio": contact.get("portfolio")
        },

        "summary": summary,

        "education": education,

        "experience": experience,

        "skills": skills,

        "projects": projects,

        "certifications": certifications,

        "languages": languages,

        "career": career,

        "quality": quality,

        "interview_context": interview_context
    }