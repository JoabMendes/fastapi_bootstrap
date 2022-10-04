PYTEST_CMD = python -m py.test
PYTEST_COVERAGE_CMD = $(PYTEST_CMD) --no-cov-on-fail --cov=app --cov-config=src/app/.coveragerc
MINIMUM_COVERAGE = 90
GIT_FETCH_MAIN_CMD = git fetch origin main:refs/remotes/origin/main

# Development

build-run:
	# Run the development server on background
	docker-compose up -d --build
	# Now head to http://0.0.0.0:5000/healthcheck

see-log-app:
	docker-compose logs app

see-log-db:
	docker-compose logs db

build-run-attached:
	# Run the development server attached showing the logs
	docker-compose up --build

stop-docker:
	docker-compose down -v

test: build-run
	docker-compose exec app $(PYTEST_CMD) -v -x  -n auto
	make stop-docker

test-matching: build-run
	docker-compose exec app $(PYTEST_CMD) -s -v -x -rs -k $(Q)

coverage: build-run
	docker-compose exec app $(PYTEST_COVERAGE_CMD)
	make stop-docker

test-coverage: build-run
	docker-compose exec app $(PYTEST_COVERAGE_CMD) --cov-report=xml
	$(GIT_FETCH_MAIN_CMD)
	diff-cover ./coverage.xml --compare-branch=main --fail-under $(MINIMUM_COVERAGE)
	make stop-docker

test-coverage-html: build-run
	docker-compose exec app $(PYTEST_COVERAGE_CMD) --cov-report=xml --cov-report=html
	$(GIT_FETCH_MAIN_CMD)
	diff-cover ./coverage.xml --compare-branch=main
	echo "Report available on htmlcov/index.html"
	make stop-docker

test-coverage-diff-html: build-run
	docker-compose exec app $(PYTEST_COVERAGE_CMD) --cov-report=xml
	$(GIT_FETCH_MAIN_CMD)
	diff-cover ./coverage.xml --compare-branch=main --html-report coverage-diff.html
	echo "Report available on htmlcov/index.html"
	make stop-docker

lint: build-run
	docker-compose exec app flake8 --exclude=*/__init__.py
	docker-compose exec app isort -c --diff . --profile black
	make stop-docker

lint-fix: build-run
	docker-compose exec app black .
	docker-compose exec app isort --atomic . --profile black
	make stop-docker

# CI

ci-lint:
	flake8 --exclude=*/__init__.py
	isort -c --diff . --profile black
