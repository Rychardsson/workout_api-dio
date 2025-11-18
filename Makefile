run-docker:
	@docker-compose up -d

stop-docker:
	@docker-compose down

create-migrations:
	@alembic revision --autogenerate -m "$(d)"

run-migrations:
	@alembic upgrade head

run:
	@uvicorn workout_api.main:app --reload
