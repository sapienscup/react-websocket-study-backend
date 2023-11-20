# Para conseguir acesso as imagens localmente
pre_configure:
	pip install keyring keyrings.google-artifactregistry-auth
	gcloud auth configure-docker southamerica-east1-docker.pkg.dev -q

# Sobe o ambiente de desenvolvimento
dev:
	docker compose up

allow-cassandra-dev:
	sudo chmod 0777 -R ./data

# Sobe o ambiente de desenvolvimento realizando o build
dev-build: pre_configure
	docker compose up --build

# Instala o gerenciador de pacotes (poetry) e a library a partir do requirements.txt
install_library: pre_configure
	pip install poetry && pip install -r requirements.txt

# Formata o código-fonte de acordo com o padrão PEP8
format:
	cd src && poetry run autopep8 --exclude="main.py" .; poetry run isort --skip=main/routes/__init__.py .

# Checa se o código-fonte está de acordo com o padrão PEP8
check_format:
	poetry run pycodestyle ./src; poetry run isort --check-only ./src

# Checa se o código-fonte possui erros de sintaxe
check_errors:
	poetry run pylint src/ --disable=all --enable=e,f

# Roda os testes unitários
test:
	ENV='test' poetry run pytest --cov-config=.coveragerc --cov-report html --cov=. src/

# Realiza deploy no AppEngine - modo de uso: make version=suaversao deploy
deploy:
	gcloud app deploy --version=$(version) --no-promote

venv:
	python3 -m venv venv 
