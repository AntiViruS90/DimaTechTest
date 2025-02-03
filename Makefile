# Два варианта запуска приложения:
	# 1. Python
	# 2. Docker compose

# Устанавливаем все зависимости и создаем БД с необходимой структурой
start:
	pip install -r requirements.txt
	python -m app.main

# Создаём тестовые данные в БД
test_data:
	python -m app.create_test_data


# Docker
# Создание БД для приложения,если таковой нет
POSTGRES_VERSION ?= 17
docker-run-db:
	docker run --name postgres_db --restart=always -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=postgres -p 5432:5432 -d postgres:$(POSTGRES_VERSION)

docker-build:
	docker-compose up --build -d