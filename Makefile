good = \033[32;1m
bad = \033[1;31m
command = \033[1;36m
clear = \033[39;49m

SHELL := /usr/bin/bash

help:
	@echo -e "$(command)make install$(clear): Sets up a virtualenv, installs deps."
	@echo -e "$(command)make start$(clear): Runs the server (for local development)."
	@echo -e "$(command)make test$(clear): Runs the tests w/ pytest."
	@echo -e "$(command)make migrations$(clear): Makes Django Migrations (does not apply them)."
	@echo -e "$(command)make migrate$(clear): Applies Django migrations (see settings.py before first run)."
	@echo -e "$(command)make loaddb$(clear): Loads the cards into the db from AllPrintings.json."
	@echo -e "$(command)make shell$(clear): Runs a local shell_plus instance."

install:
	@echo -e "** $(good)Setting up virtualenv...$(clear) **"
	python3 -m venv .collected
	@echo -e "** $(good)Installing packages...$(clear) **"
	source .collected/bin/activate && pip3 install poetry
	source .collected/bin/activate && poetry install
	@echo -e "** $(good)Done!$(clear) **"
	@echo -e "** $(good)If you haven't already, please run $(command)source .collected/bin/activate$(good) to activate the virtual environment.$(clear) **"
	@echo -e "** $(good)Finally, if you haven't, run $(command)aws configure$(good) to set up your AWS credentials.$(clear) **"

start:
	@source .collected/bin/activate && python manage.py runserver_plus

test:
	@source .collected/bin/activate && pytest
migrations:
	@source .collected/bin/activate && python manage.py makemigrations
migrate:
	@source .collected/bin/activate && python manage.py migrate
loaddb:
	@source .collected/bin/activate && python manage.py loaddb
shell:
	@source .collected/bin/activate && python manage.py shell_plus
