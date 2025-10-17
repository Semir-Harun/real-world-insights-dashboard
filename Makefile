.PHONY: setup lint format test app
setup:
	python -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt
lint:
	ruff check src tests
format:
	black src tests
test:
	pytest -q
app:
	streamlit run src/app/streamlit_app.py