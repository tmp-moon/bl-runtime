MODEL_ID=google-t5/t5-base
FRAMEWORK=transformers

run:
	python main.py --model-id $(MODEL_ID) --framework $(FRAMEWORK)

dependencies:
	pip install -r requirements.txt

python-version:
	pyenv install 3.12
	pyenv global 3.12
	python --version

env:
	pyenv activate blruntime

call:
	curl -X POST \
		http://localhost:4321/ \
		-H "Content-Type: application/json" \
		-d '{"inputs": "My name is Sarah and I live in London"}'

build:
	docker build -t sindar/toto12345 --platform linux/amd64 --push .