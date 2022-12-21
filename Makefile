MANAGE := poetry run python manage.py

.PHONY: install
install:
	poetry install

.PHONY: migrate
migrate:
	@$(MANAGE) migrate

.PHONY: setup
setup:
	make install
	make migrate
	echo "Create superuser"
	poetry run python manage.py createsuperuser

.PHONY: start
start:
	@$(MANAGE) runserver task-manager.localhost:8000

.PHONY: lint
lint:
	poetry run flake8 task_manager templates

.PHONY: test
test:
	@poetry run coverage run --source='.' manage.py test

.PHONY: check
check: lint test requirements.txt

.PHONY: test-coverage-report
test-coverage-report: test
	@poetry run coverage report -m $(ARGS)
	@poetry run coverage erase

.PHONY: test-coverage-report-xml
test-coverage-report-xml:
	poetry run coverage xml

.PHONY: secretkey
secretkey:
	poetry run python -c 'from django.utils.crypto import get_random_string; print(get_random_string(60))'

.PHONY: transprepare
transprepare:
	poetry run django-admin makemessages --locale ru --add-location file

.PHONY: transcompile
transcompile:
	poetry run django-admin compilemessages

.PHONY: requirements.txt
requirements.txt:
	poetry export --format requirements.txt --output requirements.txt --extras psycopg2 --without-hashes