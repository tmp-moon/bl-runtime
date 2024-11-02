MODEL_ID="s3://controlplane-prod-uploads/densenet161.mar"
DOCKER_IMAGE="ghcr.io/tmp-moon/runtime/torch:latest"
PLATFORM="linux/amd64"
AWS_REGION=$(shell aws configure get region)
AWS_ACCESS_KEY_ID=$(shell aws configure get aws_access_key_id)
AWS_SECRET_ACCESS_KEY=$(shell aws configure get aws_secret_access_key)
API_KEY=bl_jm6ozvbomwf9yfeyxxbyfz8i3b7s8eqb
CLIENT_CREDENTIALS=Y2hhcmxvdTpDNE01Q1JKQk5ITEE3UkRZVEk0N1RTUDZMSFdMNTA5NA==
BASE_URL=https://d19v3p57latabq.cloudfront.net
MODEL_ID=charlou/densenet161.mar
TOKEN=eyJhbGciOiJSUzI1NiIsImtpZCI6ImJlYW1saXQiLCJ0eXAiOiJKV1QifQ.eyJhdWQiOlsiYmVhbWxpdCJdLCJlbWFpbCI6ImRyYXBwaWVyLmNoYXJsZXNAZ21haWwuY29tIiwiZXhwIjoxNzMwNTE4NzMyLCJmYW1pbHlfbmFtZSI6IkRyYXBwaWVyIiwiZ2l2ZW5fbmFtZSI6IkNoYXJsZXMiLCJpYXQiOjE3MzA1MTE1MzIsImlzcyI6Imh0dHBzOi8vYXBpLmJlYW1saXQuZGV2L3YwIiwianRpIjoiWVpVMERZNkE3TFgxSUExMCIsIm5iZiI6MTczMDUxMTUzMiwic2NvcGUiOiJvZmZsaW5lX2FjY2VzcyIsInN1YiI6ImUwYmJkZjBlLTEzZjItNDMzMC1hODgyLTFhOGRmZjBlYWFmNSIsInN1Yl90eXBlIjoidXNlciJ9.XIJZ30kZ36KxTKXDEX03Zxr72inXWaTY0pE2PS_zNauKW6G2441RweB2IFcz2OpkQxudIMxmG6LbiUEQDOtCgUcO9xU0d9X1NrWnt8LHa-4Vdpe5DlRHesQ9MvIVfMcblEO7a9olNRSWF6ce9HNqAknHSU7X7XcQBtEdWYqec0CHXmltA9IkxGlTFlcA1xvsO_GCiJkQr3mqZuL4ZMNJjzWDjLHn-DkoRZc0PIOmDdPi3UQilCvTwLIF3hX2oAFuLZWEMSwXyEOAd-thTvruwb2WiYbAfqs1raISwDYNY93oDvqxMLvt5g7A8oZvdNkUwbDWR1NVsxni-lBYEkYy-2xSwpK1PxQJuL8RwwnpFxdx5lp0vUAFndKVkeakHDs76a_eQ22zJkcp7A__6rKJ8OX9K-YN38_0t6XWyehEzzLJE6qejY0rmPb0BOJUkqycM9lgwjzHEAHvaIeZJc5iRx9EtKd1ScgWX_vClZSkP1XDGvGQIxEg-BK4kGR8NRTV8SJbEL7NRKslF9ApFVMGy47Nv7uXlSAllz3prp8un6oFTmIs-E9DVcmqwnUONOKSjaOLA-s9TaMos-NFWuhYiWvBdMSmnaQqxXPbCUGLk1RUjF_9acyOF3MFMQ9WLNHFNnfbMY_gQJKK5MxYfwOnFvzhZzd__90SpghESo-hmAE

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
		--url 'https://run.beamlit.dev/charlou/models/shadow/predictions/densenet161' \
		-T samples/shadow.jpg \
		--header 'X-Beamlit-Api-Key: ${API_KEY}'
