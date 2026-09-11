import spacy


# Load local spaCy model
nlp = spacy.load(
    "en_core_web_sm"
)


def extract_entities(text):

    doc = nlp(text)

    entities = []

    for ent in doc.ents:

        entities.append({

            "text": ent.text,

            "label": ent.label_

        })

    return entities


def extract_persons(text):

    doc = nlp(text)

    return [
        ent.text
        for ent in doc.ents
        if ent.label_ == "PERSON"
    ]


def extract_organizations(text):

    doc = nlp(text)

    return [
        ent.text
        for ent in doc.ents
        if ent.label_ == "ORG"
    ]


def extract_locations(text):

    doc = nlp(text)

    return [
        ent.text
        for ent in doc.ents
        if ent.label_ in ["GPE", "LOC"]
    ]