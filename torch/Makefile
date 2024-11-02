MODEL_ID="s3://controlplane-prod-uploads/densenet161.mar"
DOCKER_IMAGE="sindar/alpha1234abcd"
PLATFORM="linux/amd64"
AWS_REGION=$(shell aws configure get region)
AWS_ACCESS_KEY_ID=$(shell aws configure get aws_access_key_id)
AWS_SECRET_ACCESS_KEY=$(shell aws configure get aws_secret_access_key)
API_KEY=bl_jm6ozvbomwf9yfeyxxbyfz8i3b7s8eqb
CLIENT_CREDENTIALS=Y2hhcmxvdTpDNE01Q1JKQk5ITEE3UkRZVEk0N1RTUDZMSFdMNTA5NA==
BASE_URL=https://d19v3p57latabq.cloudfront.net
MODEL_ID=charlou/densenet161.mar

build:
	docker build -t ${DOCKER_IMAGE} .

push:
	docker build --push --platform ${PLATFORM} -t ${DOCKER_IMAGE} .
	
run:
	docker rm -f torchserve
	docker run \
		--rm \
		--name torchserve \
		-p 80:80 \
		-p 8081:8081 \
		-e BL_CLIENT_CREDENTIALS=${CLIENT_CREDENTIALS} \
		${DOCKER_IMAGE} \
		--model-id ${BASE_URL}/${MODEL_ID}

test:
	curl http://127.0.0.1/predictions/densenet161 -T samples/shadow.jpg
	curl http://127.0.0.1/predictions/densenet161 -T samples/pixel.jpg

test-prod:
	curl --request POST \
		--url 'https://run.beamlit.dev/charlou/shadow/predictions/densenet161' \
		-T samples/shadow.jpg \
		--header 'Api-Key: ${API_KEY}'