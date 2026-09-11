# 📄 CV Parser

A Python-based CV/Resume Parser that converts unstructured resumes into structured, machine-readable JSON data.

The parser supports PDF, DOCX, JPG, JPEG, and PNG files and combines document extraction, OCR, regular expressions, rule-based parsing, and NLP to extract candidate information.

## ✨ Features

- PDF parsing
- DOCX parsing
- JPG, JPEG, and PNG image parsing
- OCR for scanned PDFs and images using PaddleOCR
- Automatic CV section detection
- Personal information extraction
- Email and phone extraction
- LinkedIn and GitHub extraction
- Education extraction
- Work experience extraction
- Skills extraction
- Projects extraction
- Certifications extraction
- Languages extraction
- NLP-based entity extraction with spaCy
- Structured JSON output

## 🧠 How It Works

```text
                    CV / Resume
                         │
                         ▼
                File Type Detection
                         │
          ┌──────────────┼──────────────┐
          ▼              ▼              ▼
         PDF            DOCX          Image
          │              │              │
       PyMuPDF       python-docx     PaddleOCR
          │
          │ Scanned PDF?
          ▼
       PaddleOCR
          │
          └──────────────┬──────────────┘
                         ▼
                   Extracted Text
                         │
                         ▼
                  Section Detection
                         │
                         ▼
              Information Extraction
                  Regex + Rules
                         │
                         ▼
                    spaCy NLP
                         │
                         ▼
                  Structured JSON
```

## 📂 Supported Input Formats

| Format | Extraction Method |
|---|---|
| `.pdf` | PyMuPDF + PaddleOCR |
| `.docx` | python-docx |
| `.jpg` | PaddleOCR |
| `.jpeg` | PaddleOCR |
| `.png` | PaddleOCR |

For normal PDFs, the parser first attempts direct text extraction. If very little text is detected, the PDF is treated as potentially scanned and its pages are processed with OCR.

## 🔍 Processing Pipeline

### 1. Document Extraction

- **PDF:** PyMuPDF is used for text-based PDFs. Scanned PDFs can be processed with PaddleOCR.
- **DOCX:** Paragraphs and tables are extracted using python-docx.
- **Images:** PaddleOCR extracts text from JPG, JPEG, and PNG files.

### 2. Section Detection

The parser identifies common CV sections such as:

```text
SUMMARY
EDUCATION
EXPERIENCE
SKILLS
PROJECTS
CERTIFICATIONS
LANGUAGES
```

It also supports common variations such as Professional Summary, Academic Background, Work Experience, Professional Experience, Technical Skills, Personal Projects, Certificates, and Language Skills.

### 3. Information Extraction

After section detection, specialized parsing logic extracts information from each section.

## 🎓 Education Extraction

The education parser handles different CV layouts, including:

```text
2021 - 2025
Zagazig University
Bachelor of Computer Science
```

and:

```text
Zagazig University
Bachelor of Computer Science
2021 - 2025
```

and:

```text
Zagazig University — Faculty of Computers and Informatics | 2025 – Present
Bachelors in Computer Science — Egypt, Cairo
```

It attempts to extract:

- Degree
- Institution
- Field
- Start date
- End date
- GPA

Example:

```json
{
  "degree": "Bachelors",
  "institution": "Zagazig University",
  "field": "Computer Science",
  "start_date": "2025",
  "end_date": "Present",
  "gpa": null
}
```

## 💼 Experience Extraction

The experience parser identifies job entries and extracts:

- Job title
- Company
- Start date
- End date
- Description
- Technologies

Example:

```text
Data Engineering Track – DEPI | 08/2026 – Present
• Undertook intensive training...
• Worked with SQL and databases...
```

Example output:

```json
{
  "job_title": "Data Engineering Track",
  "company": "DEPI",
  "location": null,
  "start_date": "08/2026",
  "end_date": "Present",
  "description": [
    "Undertook intensive training...",
    "Worked with SQL and databases..."
  ],
  "technologies": []
}
```

## 📧 Contact Information

Regular expressions are used to extract:

- Email addresses
- Phone numbers
- LinkedIn profiles
- GitHub profiles
- URLs

Example:

```json
{
  "email": "example@gmail.com",
  "phone": "01000000000",
  "linkedin": "linkedin.com/in/example",
  "github": "github.com/example"
}
```

## 🧠 NLP

The project uses spaCy for Natural Language Processing and Named Entity Recognition.

Supported entity types include:

```text
PERSON
ORG
GPE
LOC
```

The parser does not depend on an external generative AI API for its core extraction. Instead, it combines:

```text
Regex
   +
Rule-Based Parsing
   +
spaCy NLP
   +
OCR
```

This makes the extraction process more controllable and explainable.

## 📦 JSON Output

The final parsed CV is stored as structured JSON.

Example:

```json
{
  "personal_information": {
    "name": "Mahmoud Ahmed Tarek",
    "email": "example@gmail.com",
    "phone": "01000000000",
    "linkedin": "linkedin.com/in/example",
    "github": "github.com/example"
  },
  "summary": "AI & Machine Learning Trainee...",
  "education": [
    {
      "degree": "Bachelors",
      "institution": "Zagazig University",
      "field": "Computer Science",
      "start_date": "2025",
      "end_date": "Present",
      "gpa": null
    }
  ],
  "experience": [
    {
      "job_title": "Data Engineering Track",
      "company": "DEPI",
      "location": null,
      "start_date": "08/2026",
      "end_date": "Present",
      "description": [
        "Undertook intensive training..."
      ],
      "technologies": []
    }
  ],
  "skills": [],
  "projects": [],
  "certifications": [],
  "languages": []
}
```

## 🏗️ Project Structure

```text
CV-Parser/
│
├── document_parser.py
│   └── PDF, DOCX, and image text extraction
│
├── section_detector.py
│   └── CV section detection and splitting
│
├── regex_extractor.py
│   └── Contact information extraction
│
├── nlp_parser.py
│   └── spaCy NLP and entity extraction
│
├── json_builder.py
│   └── Structured CV information generation
│
├── main.py
│   └── Main application
│
├── requirements.txt
├── README.md
│
└── output/
    └── parsed_cv.json
```

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| **Python** | Core programming language |
| **PyMuPDF** | PDF text extraction |
| **python-docx** | DOCX text and table extraction |
| **PaddleOCR** | OCR for images and scanned PDFs |
| **spaCy** | NLP and Named Entity Recognition |
| **Regular Expressions** | Contact and pattern extraction |
| **JSON** | Structured output |

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/CV-Parser.git
cd CV-Parser
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Download the spaCy model

```bash
python -m spacy download en_core_web_sm
```

## ▶️ Usage

Set the CV path in the main program:

```python
file_path = r"E:\CVs\resume.pdf"
```

Then run:

```bash
python main.py
```

The parser will:

1. Detect the file type
2. Extract the text
3. Run OCR if necessary
4. Detect CV sections
5. Extract structured information
6. Build the JSON object
7. Save the result as JSON

## 🖼️ Multiple Images

Multiple CV pages/images can be combined before parsing:

```python
file_paths = [
    r"E:\CVs\page1.png",
    r"E:\CVs\page2.png"
]

text = ""

for file_path in file_paths:
    text += extract_from_file(file_path) + "\n"
```

## 🎯 Project Goal

The goal of this project is to transform **unstructured CV documents into structured data** that can be consumed by software systems.

This creates a foundation for applications such as:

- Applicant Tracking Systems (ATS)
- Candidate management systems
- Resume databases
- CV search engines
- Job matching systems
- Candidate ranking
- Resume analysis
- Recruitment platforms
- Automated recruitment pipelines

## 🚀 Potential Applications

The structured JSON output can be integrated into larger recruitment and data-processing systems.

For example:

```text
CV Upload
    │
    ▼
CV Parser
    │
    ▼
Structured JSON
    │
    ├── ATS
    ├── Candidate Database
    ├── Job Matching
    ├── Resume Analysis
    └── Candidate Ranking
```

## 🔮 Future Improvements

- [ ] More robust CV layout handling
- [ ] Better job title and company detection
- [ ] Automatic technology extraction
- [ ] Skill normalization
- [ ] Improved date recognition
- [ ] Better name extraction
- [ ] ATS compatibility scoring
- [ ] Job description matching
- [ ] Candidate ranking
- [ ] REST API using FastAPI
- [ ] Web interface for CV upload
- [ ] Database integration
- [ ] Support for additional document formats

## 📌 Current Approach

The parser currently follows a **hybrid extraction approach**:

```text
             CV
              │
              ▼
       Document Extraction
              │
              ▼
       OCR (when required)
              │
              ▼
       Section Detection
              │
       ┌──────┴──────┐
       ▼             ▼
     Regex        Rule-Based
       │             │
       └──────┬──────┘
              ▼
          spaCy NLP
              │
              ▼
       Structured JSON
```

The project does not require an external generative AI API for its core CV extraction.

## 👨‍💻 Author

**Mahmoud Ahmed Tarek**

**AI & Machine Learning Trainee | Aspiring Data Engineer**

---

⭐ If you find this project useful, consider giving the repository a star.
