line_length = 120
coding_style_command = poetry run black -l $(line_length) src test fixture

.PHONY: help code_style code_style_fix linter test ci question stats type-check unused-code

help: ## Show Help
	@printf "\033[0;33mFrench highway code test makefile\033[0m\n\n"
	@printf "usage: make | [target]\n\n"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

code-style: ## Check code style
	$(coding_style_command) --check --diff

code-style-fix: ## Fix code style
	$(coding_style_command)

linter: ## Check code linter
	poetry run flake8 --max-line-length $(line_length) --max-complexity 5 src test fixture
	poetry run pylint --max-line-length $(line_length) src test fixture

test: ## Run test
	poetry run pytest --cache-clear

type-check: ## Run static type checking
	MYPYPATH=src poetry run mypy --namespace-packages --explicit-package-bases src test fixture

unused-code: ## Check unused code
	poetry run autoflake -cd --remove-all-unused-imports --remove-unused-variables -r src test fixture

unused-code-fix: ## Fix unused code
	poetry run autoflake -i --remove-all-unused-imports --remove-unused-variables -r src test fixture

security-issue: ## Check security issue
	poetry run bandit -ril src

ci: code-style unused-code security-issue linter type-check test ## Run CI test

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
