.PHONY: lint format

help:
	@echo "lint - check style with black, flake8, sort python with isort, and indent html"
	@echo "format - enforce a consistent code style across the codebase and sort python files with isort"

lint-server:
	black --target-version py37 --check --diff .
	flake8
	isort --check-only --diff .
	curlylint --parse-only bakerydemo
	git ls-files '*.html' | xargs djhtml --check

lint-client:
	npm run lint:css --silent
	npm run lint:js --silent
	npm run lint:format --silent

lint: lint-server lint-client

format-server:
	black --target-version py37 .
	isort .
	git ls-files '*.html' | xargs djhtml -i

format-client:
	npm run format
	npm run fix:js

format: format-server format-client

benchmark: export DJANGO_SETTINGS_MODULE = bakerydemo.settings.test
benchmark: export DATABASE_URL = sqlite:///benchmark.db
benchmark:
	rm -rf benchmark.db
	mkdir -p benchmarks
	python manage.py migrate
	python manage.py load_initial_data
	python manage.py collectstatic --no-input
	python manage.py runserver $${BENCHMARK_PORT:-8453} & echo $$! > benchmark_server.pid
	-pytest --html=benchmarks/report-`python3 -c "import django; print(django.get_version())"`-`python3 -c "import wagtail; print(wagtail.get_version(wagtail.VERSION))"`.html --self-contained-html --headed
	kill `cat benchmark_server.pid`
	rm benchmark_server.pid
