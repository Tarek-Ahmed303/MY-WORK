import re


def extract_email(text):

    pattern = (
        r"\b[A-Za-z0-9._%+-]+"
        r"@[A-Za-z0-9.-]+\."
        r"[A-Za-z]{2,}\b"
    )

    match = re.search(
        pattern,
        text
    )

    if match:
        return match.group(0)

    return None


def extract_phone(text):

    pattern = (
        r"(?<!\d)"
        r"(?:\+\d{1,3}[\s.-]?)?"
        r"(?:\(?\d{2,4}\)?[\s.-]?)?"
        r"\d{3,4}[\s.-]?"
        r"\d{3,4}"
        r"(?!\d)"
    )

    matches = re.findall(
        pattern,
        text
    )

    if matches:

        return matches[0].strip()

    return None


def extract_linkedin(text):

    pattern = (
        r"(?:https?://)?"
        r"(?:www\.)?"
        r"linkedin\.com/[^\s]+"
    )

    match = re.search(
        pattern,
        text,
        re.IGNORECASE
    )

    if match:
        return match.group(0)

    return None


def extract_github(text):

    pattern = (
        r"(?:https?://)?"
        r"(?:www\.)?"
        r"github\.com/[^\s]+"
    )

    match = re.search(
        pattern,
        text,
        re.IGNORECASE
    )

    if match:
        return match.group(0)

    return None


def extract_urls(text):

    pattern = (
        r"https?://[^\s]+"
    )

    return re.findall(
        pattern,
        text
    )


def extract_contact_information(text):

    return {

        "email": extract_email(text),

        "phone": extract_phone(text),

        "linkedin": extract_linkedin(text),

        "github": extract_github(text)
    }