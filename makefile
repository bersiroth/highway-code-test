line_length = 120
coding_style_command = black -l $(line_length) src test

.PHONY: help code_style code_style_fix linter test ci question stats

help: ## Show Help
	@printf "\033[0;33mFrench highway code test makefile\033[0m\n\n"
	@printf "usage: make | [target]\n\n"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

code_style: ## Check code style
	$(coding_style_command) --check --diff

code_style_fix: ## Fix code style
	$(coding_style_command)

linter: ## Check code linter
	flake8 --max-line-length $(line_length) --max-complexity 5 src test
	PYTHONPATH=src pylint --max-line-length $(line_length) src test

test: ## Run test
	pytest --cache-clear

type-check: ## Run static type checking
	MYPYPATH=src mypy --namespace-packages --explicit-package-bases src test

ci: code_style linter type-check test ## Run CI test

question: ## Run question command
	python3 src/command.py question

stats: ## Run stats command
	python3 src/command.py stats
