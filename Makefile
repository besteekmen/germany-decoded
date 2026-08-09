setup:
	docker compose build
	docker compose up -d postgres
	docker compose run --rm app python -m germany_decoded.db.init
	docker compose run --rm app python -m germany_decoded.index
	docker compose up -d app

build:
	docker compose build

up:
	docker compose up -d

down:
	docker compose down

ps:
	docker compose ps

logs:
	docker compose logs -f app

psql:
	docker compose exec postgres sh -c 'psql -U "$$POSTGRES_USER" -d "$$POSTGRES_DB"'

reset-db:
	docker compose run --rm app python -c "from germany_decoded.db.init import init_db; init_db(drop=True)"

init-db:
	docker compose run --rm app python -m germany_decoded.db.init

index:
	docker compose run --rm app python -m germany_decoded.index

cli:
	docker compose run --rm app python -m germany_decoded.main

app:
	docker compose up -d app

eval-retrieval:
	docker compose run --rm app python -m germany_decoded.evaluation.retrieval_eval

eval-judge:
	docker compose run --rm app python -m germany_decoded.evaluation.judge_eval

eval-rag:
	docker compose run --rm app python -m germany_decoded.evaluation.rag_eval

eval-all:
	$(MAKE) eval-retrieval
	$(MAKE) eval-rag
	$(MAKE) eval-judge
debug-retrieval:
	docker compose run --rm app python -m germany_decoded.evaluation.debug_retrieval