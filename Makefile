start:
	uvicorn mcqa.llm_api:app --reload

setup:
	poetry install

format:
	poetry run black .
	poetry run isort .

lint:
	poetry run flake8 .
	poetry isort -check-only .

clean:
	find . -name __pycache__ -type d -exec rm -r {} \+
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf .coverage
	rm -rf ./dist
