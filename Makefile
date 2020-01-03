setup:
	pip3 install --user pipenv
	pipenv sync --dev
update:
	pipenv --rm
	pipenv update
	pipenv run pip freeze > requirements.txt
update-dev:
	pipenv --rm
	pipenv update --dev
	pipenv run pip freeze > requirements.txt
lint:
	pipenv run pre-commit install -f --install-hooks
	pipenv run pre-commit run --all-files
install-dev:
	pip3 install --user pipenv
	pipenv sync
	pipenv run pip install -e .
release:
	python3 -m pip install --user pipenv
	pipenv run python3 -m pip install --upgrade setuptools wheel twine
	pipenv run python3 setup.py sdist bdist_wheel
	#python3 -m twine upload dist/*
