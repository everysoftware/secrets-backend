.PHONY: up
up:
	docker-compose up --build -d

.PHONY: up-prod
up-prod:
	docker-compose -f docker-compose.yml -f docker-compose-prod.yml up --build -d

.PHONY: logs
logs:
	docker-compose logs --since 10m --follow

.PHONY: stop
stop:
	docker-compose stop

.PHONY: restart
restart:
	docker-compose restart

.PHONY: format
format:
	ruff format .

.PHONY: lint
lint:
	ruff check . --fix
	mypy . --install-types --enable-incomplete-feature=NewGenericSyntax

PHONY: generate
generate:
	docker-compose up db -d
	alembic revision --autogenerate

PHONY: upgrade
upgrade:
	docker-compose up db -d
	alembic upgrade head

PHONY: downgrade
downgrade:
	docker-compose up db -d
	alembic downgrade -1

# Windows only
PHONY: kill
kill:
	TASKKILL /F /IM python.exe
