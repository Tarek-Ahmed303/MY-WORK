# Question Generation System — Project Flow

```text
Question_Generation/
│
├── knowledge_base/
│   ├── questions/
│   │   │
│   │   ├── ai_ml/
│   │   │   ├── machine_learning.md
│   │   │   ├── deep_learning.md
│   │   │   ├── nlp.md
│   │   │   ├── computer_vision.md
│   │   │   └── llm_rag.md
│   │   │
│   │   ├── data_science/
│   │   │   ├── statistics.md
│   │   │   ├── data_analysis.md
│   │   │   └── data_science.md
│   │   │
│   │   ├── backend/
│   │   │   ├── python.md
│   │   │   ├── django.md
│   │   │   ├── fastapi.md
│   │   │   ├── databases.md
│   │   │   └── rest_api.md
│   │   │
│   │   ├── frontend/
│   │   ├── devops/
│   │   ├── cloud/
│   │   ├── cybersecurity/
│   │   │
│   │   ├── cs_fundamentals/
│   │   │   ├── oop.md
│   │   │   ├── data_structures.md
│   │   │   ├── algorithms.md
│   │   │   ├── operating_systems.md
│   │   │   ├── networking.md
│   │   │   └── databases.md
│   │   │
│   │   ├── hr/
│   │   │   ├── general.md
│   │   │   ├── motivation.md
│   │   │   └── career.md
│   │   │
│   │   └── behavioral/
│   │       ├── teamwork.md
│   │       ├── leadership.md
│   │       ├── conflict.md
│   │       └── problem_solving.md
│   │
│   └── README.md
│
├── ingestion/
│   ├── markdown_loader.py
│   ├── question_parser.py
│   ├── metadata_extractor.py
│   ├── document_builder.py
│   └── ingestion_pipeline.py
│
├── embeddings/
│   ├── embedder.py
│   └── embedding_config.py
│
├── vector_store/
│   ├── vector_store.py
│   ├── index_builder.py
│   └── metadata_filter.py
│
├── rag/
│   ├── query_builder.py
│   ├── retriever.py
│   ├── reranker.py
│   └── rag_engine.py
│
├── context/
│   ├── candidate_context.py
│   ├── job_context.py
│   ├── interview_context.py
│   └── context_builder.py
│
├── generation/
│   ├── prompt_builder.py
│   ├── llm_client.py
│   └── question_generator.py
│
├── validation/
│   └── question_validator.py
│
├── selection/
│   ├── question_selector.py
│   ├── duplicate_detector.py
│   └── diversity_filter.py
│
├── models/
│   ├── question.py
│   ├── question_context.py
│   ├── interview_state.py
│   └── generation_result.py
│
├── pipeline/
│   └── question_engine.py
│
├── tests/
│   ├── test_knowledge_base.py
│   ├── test_ingestion.py
│   ├── test_retrieval.py
│   ├── test_generation.py
│   ├── test_validation.py
│   ├── test_selection.py
│   └── test_pipeline.py
│
├── main.py
├── requirements.txt
└── README.md
```

## System Flow

```text
Knowledge Base
      │
      ▼
Markdown Loader
      │
      ▼
Question Parser
      │
      ▼
Metadata Extraction
      │
      ▼
Document Builder
      │
      ▼
Ingestion Pipeline
      │
      ▼
Embedding Model
      │
      ▼
Vector Store
      │
      ▼
────────────────────────────────────
          USER / INTERVIEW
────────────────────────────────────
      │
      ▼
Candidate Context
      │
      ├── Job Context
      │
      └── Interview Context
      │
      ▼
Context Builder
      │
      ▼
Query Builder
      │
      ▼
Retriever
      │
      ▼
Reranker
      │
      ▼
RAG Engine
      │
      ▼
Prompt Builder
      │
      ▼
LLM Client
      │
      ▼
Question Generator
      │
      ▼
Question Validator
      │
      ▼
Duplicate Detector
      │
      ▼
Diversity Filter
      │
      ▼
Question Selector
      │
      ▼
Question Engine
      │
      ▼
Final Interview Question
```

## Main Responsibility of Each Layer

### 1. Knowledge Base
Contains the source questions organized by Computer Science and interview categories.

### 2. Ingestion
Reads the Markdown question files, parses questions, extracts metadata, and converts them into documents ready for embedding.

### 3. Embeddings
Converts questions and documents into vector representations for semantic search.

### 4. Vector Store
Stores embeddings and metadata and provides similarity-based retrieval and metadata filtering.

### 5. RAG
Builds the retrieval query, retrieves relevant questions, reranks them, and prepares the retrieved knowledge for generation.

### 6. Context
Combines information about the candidate, job, and current interview state to make question generation contextual.

### 7. Generation
Builds the LLM prompt, communicates with the LLM, and generates candidate interview questions.

### 8. Validation
Checks generated questions for quality, relevance, structure, and other required constraints.

### 9. Selection
Removes duplicates, improves question diversity, and selects the most appropriate question for the interview.

### 10. Pipeline
Orchestrates the complete process from context and retrieval to the final question.

### 11. Tests
Tests each layer independently and validates the complete question-generation pipeline.

## End-to-End Pipeline

```text
                 ┌─────────────────────┐
                 │   Question Database │
                 │   / Knowledge Base  │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │      Ingestion      │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │     Embeddings      │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │    Vector Store     │
                 └──────────┬──────────┘
                            │
                            │
 Candidate ───────────────┐  │
 Job ────────────────────┼──┤
 Interview State ────────┘  │
                            ▼
                 ┌─────────────────────┐
                 │   Context Builder   │
                 └──────────┬──────────┘
                            ▼
                 ┌─────────────────────┐
                 │    Query Builder    │
                 └──────────┬──────────┘
                            ▼
                 ┌─────────────────────┐
                 │      Retriever      │
                 └──────────┬──────────┘
                            ▼
                 ┌─────────────────────┐
                 │      Reranker       │
                 └──────────┬──────────┘
                            ▼
                 ┌─────────────────────┐
                 │    RAG Engine       │
                 └──────────┬──────────┘
                            ▼
                 ┌─────────────────────┐
                 │   Prompt Builder    │
                 └──────────┬──────────┘
                            ▼
                 ┌─────────────────────┐
                 │    LLM Client       │
                 └──────────┬──────────┘
                            ▼
                 ┌─────────────────────┐
                 │ Question Generator  │
                 └──────────┬──────────┘
                            ▼
                 ┌─────────────────────┐
                 │ Question Validator  │
                 └──────────┬──────────┘
                            ▼
                 ┌─────────────────────┐
                 │ Duplicate Detector  │
                 └──────────┬──────────┘
                            ▼
                 ┌─────────────────────┐
                 │  Diversity Filter   │
                 └──────────┬──────────┘
                            ▼
                 ┌─────────────────────┐
                 │  Question Selector  │
                 └──────────┬──────────┘
                            ▼
                 ┌─────────────────────┐
                 │   Final Question    │
                 └─────────────────────┘
```
