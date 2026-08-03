up:
	docker compose up -d

down:
	docker compose down

psql:
	docker exec -it germany-decoded-db psql -U admin -d germany_decoded

reset-db:
	uv run python -c "from germany_decoded.db.init import init_db; init_db(drop=True)"

init-db:
	uv run python -m germany_decoded.db.init

index:
	uv run python -m germany_decoded.index

cli:
	uv run python -m germany_decoded.main

app:
	uv run streamlit run app_new.py

monitor:
	uv run streamlit run admin.py

eval-retrieval:
	uv run python -m germany_decoded.evaluation.retrieval_eval

eval-judge:
	uv run python -m germany_decoded.evaluation.judge_eval

debug-retrieval:
	uv run python -m germany_decoded.evaluation.debug_retrieval