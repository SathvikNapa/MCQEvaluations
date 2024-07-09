start:
	uvicorn mcqa.llm_api:app --reload

setup:
	pip install -r requirements.txt
