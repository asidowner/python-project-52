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

.PHONY: start
start:
	@$(MANAGE) runserver 0.0.0.0:8000

.PHONY: check
check:
	poetry check

.PHONY: lint
lint:
	poetry run flake8 task_manager templates

.PHONY: test
test:
	@$(MANAGE) test

.PHONY: secretkey
secretkey:
	poetry run python -c 'from django.utils.crypto import get_random_string; print(get_random_string(60))'

.PHONY: trans-prepare
trans-prepare:
	@$(MANAGE) makemessages --locale ru --add-location file

.PHONY: trans-compile
trans-compile:
	@$(MANAGE) compilemessages