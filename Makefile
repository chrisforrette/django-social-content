lint:
	flake8 social_content

test:
	py.test --cov social_content -s -rxs ./social_content/tests/

setup:
	pip install -r requirements.txt

.PHONY: lint test setup
