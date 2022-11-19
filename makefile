line_length = 120
coding_style_command = poetry run black -l $(line_length) src tests fixture

.PHONY: help code_style code_style_fix linter test ci question stats type-check unused-code

help: ## Show Help
	@printf "\033[0;33mFrench highway code test makefile\033[0m\n\n"
	@printf "usage: make | [target]\n\n"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

code-style: ## Check code style
	$(coding_style_command) --check --diff

code-style-fix: ## Fix code style
	$(coding_style_command)

import: ## Check import
	poetry run isort --check --diff src tests fixture

import-fix: ## Fix import
	poetry run isort src tests fixture

linter: ## Check code linter
	poetry run flake8 --max-line-length $(line_length) --max-complexity 8 src tests fixture
	poetry run pylint --max-line-length $(line_length) --rcfile=.pylintrc src tests fixture

test-unit: ## Run unit tests
	poetry run pytest --cache-clear tests/unit

test-functional: ## Run functional tests
	poetry run pytest --cache-clear tests/functional

test-all: ## Run all tests
	poetry run pytest --cache-clear tests

test-functional-coverage: ## Run functional tests
	poetry run coverage run --include='src/highway_code/infrastructure/cli/*,src/highway_code/infrastructure/containers.py' --rcfile=.coveragerc -m pytest --cache-clear tests/functional
	make coverage-report

test-unit-coverage: ## Run unit test with coverage
	poetry run coverage run --source=src --omit='src/highway_code/infrastructure/cli/*,src/highway_code/infrastructure/persistence/*,src/highway_code/infrastructure/containers.py' --rcfile=.coveragerc -m pytest --cache-clear tests/unit
	make coverage-report

coverage-report: ## Generate coverage report
	poetry run coverage report -m --skip-covered --fail-under=100

type-check: ## Run static type checking
	MYPYPATH=src poetry run mypy --namespace-packages --strict --explicit-package-bases src tests fixture

unused-code: ## Check unused code
	poetry run autoflake -cd --remove-all-unused-imports --remove-unused-variables -r src tests fixture

unused-code-fix: ## Fix unused code
	poetry run autoflake -i --remove-all-unused-imports --remove-unused-variables -r src tests fixture

security-issue: ## Check security issue
	poetry run bandit -ril src

security-dependency: ## Check dependency security issue
	poetry run pip freeze | poetry run safety check --stdin

ci: code-style ## Run CI test
ci: unused-code
ci: security-dependency
ci: security-issue
ci: import
ci: linter
ci: type-check
ci: test-all-coverage

fix: code-style-fix ## fix code base
fix: import-fix
fix: unused-code-fix

update-translation: ## Update translation file
	xgettext -d base -o locales/base.pot src/*.py
	msgmerge --update locales/en/LC_MESSAGES/main.po locales/base.pot
	msgmerge --update locales/fr/LC_MESSAGES/main.po locales/base.pot

build-translation: ## Build translation file
	msgfmt locales/en/LC_MESSAGES/main.po -o locales/en/LC_MESSAGES/main.mo
	msgfmt locales/fr/LC_MESSAGES/main.po -o locales/fr/LC_MESSAGES/main.mo

build: ## Build package
	poetry build

question: ## Run question command
	poetry run highway-code question

stats: ## Run stats command
	poetry run highway-code stats
