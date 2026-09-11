import re


def clean_text(text):

    # Normalize line endings
    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    # Remove excessive spaces
    text = re.sub(
        r"[ \t]+",
        " ",
        text
    )

    # Remove excessive blank lines
    text = re.sub(
        r"\n{3,}",
        "\n\n",
        text
    )

    # Remove spaces at beginning/end
    lines = []

    for line in text.split("\n"):

        line = line.strip()

        if line:
            lines.append(line)

    return "\n".join(lines)