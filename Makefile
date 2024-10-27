MODEL_ID=google-t5/t5-base
FRAMEWORK=transformers
DOCKER_IMAGE=sindar/toto12345
TAG=v1

run:
	python main.py --model-id $(MODEL_ID) --framework $(FRAMEWORK)

dependencies:
	pip install torch --index-url https://download.pytorch.org/whl/cpu
	pip install diffusers transformers fastapi uvicorn accelerate>=0.26.0

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
	docker build -t ${DOCKER_IMAGE}:${TAG} --platform linux/amd64 --push .


docker-run:
	docker rm -f blruntime
	docker run \
		--rm \
		--platform linux/amd64 \
		--name blruntime \
		-p 4321:4321 \
		${DOCKER_IMAGE}:${TAG} \
		--model-id $(MODEL_ID) \
		--framework $(FRAMEWORK)