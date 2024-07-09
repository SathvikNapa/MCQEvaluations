# Cancer MCQ Answers LLM Evaluations

This repository aims to evaluate the LLM responses for MCQs for Cancer related questions

## Setup

1. Create a new virtual_env and activate

```commandline
    python3 -m venv <env_name>
    source <env_name>/bin/activate
```

2. Install the dependencies

```commandline
    pip install -r requirements.txt
```

3. Set environment variables

Refer to the `.env.example` file and create a `.env` file with the required environment variables

```commandline
    set -a
    source .env
    set +a
```

# Run the service

```commandline
    make start
```

# To test the functionality for one query

1. Start the server `make start`
2. Navigate to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
3. Click on the `Try it out` under `/generate_response` endpoint
4. Send a query with the `query_text` field
5. Example Query if the pdf is within data/Dataset_Eval/PubMed_Pdfs folder

Synthetic Response Payload

```json
{
  "query": "Which radionuclide was first used to noninvasively assess left ventricular ejection fraction and regional wall motion?",
  "options": "A. 99mTc-sestamibi B. Thallium-201 (201Tl) C. Potassium-43 (43K) D. 99mTc-labeled human serum albumin E. Rubidium-82 (82Rb) F. 13N-ammonia G. 18F-FDG H. 15O-water",
  "answer": "D. 99mTc-labeled human serum albumin",
  "question_format": "synthetic",
  "context": {
    "context_type": "pdf",
    "link_or_text": "data/Dataset_Eval/PubMed_Pdfs/1.pdf"
  }
}
```

Rephrase Response Payload

```json
{
  "query": "Which radionuclide was first used to noninvasively assess left ventricular ejection fraction and regional wall motion?",
  "options": "A. 99mTc-sestamibi B. Thallium-201 (201Tl) C. Potassium-43 (43K) D. 99mTc-labeled human serum albumin E. Rubidium-82 (82Rb) F. 13N-ammonia G. 18F-FDG H. 15O-water",
  "answer": "D. 99mTc-labeled human serum albumin",
  "question_format": "rephrase",
  "context": {
    "context_type": "pdf",
    "link_or_text": "data/Dataset_Eval/PubMed_Pdfs/1.pdf"
  }
}
```

Raw Response Payload

```json
{
  "query": "Which radionuclide was first used to noninvasively assess left ventricular ejection fraction and regional wall motion?",
  "options": "A. 99mTc-sestamibi B. Thallium-201 (201Tl) C. Potassium-43 (43K) D. 99mTc-labeled human serum albumin E. Rubidium-82 (82Rb) F. 13N-ammonia G. 18F-FDG H. 15O-water",
  "answer": "D. 99mTc-labeled human serum albumin",
  "question_format": "raw",
  "context": {
    "context_type": "pdf",
    "link_or_text": "data/Dataset_Eval/PubMed_Pdfs/1.pdf"
  }
}
```

