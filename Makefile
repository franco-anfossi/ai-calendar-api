# Variables
PYTHON = poetry run
PIP = poetry run pip

# Comandos generales
.PHONY: help install install-prod test lint format run-dev db-migrate db-upgrade db-rollback db-rollback-to update-deps

# Ayuda: Muestra todos los comandos disponibles
help:
	@echo "Comandos disponibles:"
	@echo "  make install          - Instala todas las dependencias del proyecto"
	@echo "  make install-prod     - Instala solo las dependencias de producción"
	@echo "  make test             - Ejecuta las pruebas"
	@echo "  make lint             - Ejecuta Ruff para revisar el código"
	@echo "  make format           - Formatea el código con Ruff"
	@echo "  make run-dev          - Ejecuta la aplicación en modo desarrollo"
	@echo "  make db-migrate       - Crea una nueva migración con Alembic (usa msg='mensaje')"
	@echo "  make db-upgrade       - Aplica las migraciones a la base de datos"
	@echo "  make db-rollback      - Revertir la última migración (usa steps=N)"
	@echo "  make db-rollback-to   - Revertir hasta una versión específica (usa version='id')"
	@echo "  make update-deps      - Actualiza las dependencias del proyecto"

# Instalar todas las dependencias
install:
	poetry install

# Instalar solo las dependencias de producción
install-prod:
	poetry install --no-dev

# Ejecutar las pruebas con pytest
test:
	$(PYTHON) pytest

# Lint del código usando Ruff
lint:
	$(PYTHON) ruff check .

# formatear el código con Ruff
format:
	$(PYTHON) ruff format .

# Ejecutar la aplicación con base de fastapi
run-dev:
	$(PYTHON) fastapi dev src/main.py

#Crear una nueva migración con Alembic
# Utiliza: make db-migrate msg="mensaje de la migración"
db-migrate:
	@if [ -z "$(msg)" ]; then echo "Error: Debes especificar un mensaje con msg='mensaje de la migración'"; exit 1; fi
	$(PYTHON) alembic revision --autogenerate -m "$(msg)"

# Aplicar las migraciones a la base de datos
db-upgrade:
	$(PYTHON) alembic upgrade head

# Revertir la última migración (por defecto 1)
# Utiliza: make db-rollback steps=N
db-rollback:
	@if [ -z "$(steps)" ]; then steps=1; fi; \
	$(PYTHON) alembic downgrade -$${steps}

# Revertir hasta una versión específica
# Utiliza: make db-rollback-to version="id de la migración"
db-rollback-to:
	@if [ -z "$(version)" ]; then echo "Error: Debes especificar una versión con version='id de la migración'"; exit 1; fi
	$(PYTHON) alembic downgrade $(version)

# Actualizar dependencias
update-deps:
	poetry update

# generar estructura de la api
structure:
	$(PYTHON) python generate_structure.py