hooks:
	pipenv run pre-commit run --all-files
update:
	pipenv --rm
	pipenv update
	pipenv run pip freeze > requirements.txt
lint:
	pipenv run pre-commit run --all-files
release:
	python3 -m pip install --user --upgrade setuptools wheel twine
	pipenv run python3 setup.py sdist bdist_wheel
	python3 -m twine upload dist/*
