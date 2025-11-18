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

test:
	@pytest tests/ -v

test-cov:
	@pytest tests/ -v --cov=workout_api --cov-report=html

install:
	@pip install -r requirements.txt

install-dev:
	@pip install -r requirements.txt -r requirements-dev.txt

clean:
	@find . -type d -name __pycache__ -exec rm -rf {} +
	@find . -type f -name "*.pyc" -delete
