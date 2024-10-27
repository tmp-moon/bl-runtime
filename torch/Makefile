MODEL_URL="https://test-model-beamlit.s3.eu-west-3.amazonaws.com/densenet161.mar"
MODEL_S3_URL="s3://test-model-beamlit/densenet161.mar"
DOCKER_IMAGE="sindar/alpha1234abcd"
MODEL_FILE="tmp/model-store/model.mar"
PLATFORM="linux/amd64"
AWS_REGION=$(shell aws configure get region)
AWS_ACCESS_KEY_ID=$(shell aws configure get aws_access_key_id)
AWS_SECRET_ACCESS_KEY=$(shell aws configure get aws_secret_access_key)
S3_PRESIGNED_URL=https://controlplane-prod-uploads.s3.eu-west-3.amazonaws.com/chris/charlou/densenet161.mar?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ASIAZI2LGCNYBWBTMJME%2F20241026%2Feu-west-3%2Fs3%2Faws4_request&X-Amz-Date=20241026T194606Z&X-Amz-Expires=900&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEKT%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLXdlc3QtMiJIMEYCIQCD0CbJWjXMNmtvzhwJ4bCZiVo2GpVVY2f7hKfl4yn06wIhAK%2F8DIx0QLbbjOe%2FcJsFyDfhlH22x1eVWb97BIVq9nxxKpEDCB0QABoMNjM3NDIzNDU3MTM2IgxOcBQnlcQ12FpjiZwq7gKPT%2BT%2FfScSY8zYerD%2FAp0WRUJcSxLonp94lzL3EZxQicnNI2YijaFBzj5FLYKFD3TJE12YJP9bMo2GkCGJraUuUCkPrCMtXslH1pnjLlqukpiCfT6cX3913f7BWP8Hm7p9Aw7fGJzOmE%2BAl%2FwatoxtZQNLj9k4paIR6ePkLjqWcs5oON7Zw6UmiwA5TGl2BOXp%2BDp%2F0AmRtdRsobL6ZMiEPYFjMGoEgrANtekxmV2UX9iJFf2n25pqb4L98QwusTEctORTYu2Zlux97dgkjqtMo97CNFHxTaIGQPvbOD%2FPy2usJmws5Bi53Ld%2BCuDLWS%2BuRyQhBhDp34k0ibRArAznuljyZ60IkiskWjfCSKxzqCYeo%2FRamOqut132ICssAYg5tawc88Ql81FquazVTwV4vzTai%2FgivOSFnONvJAzZOrBVQMrWUI0Z8ZEoybfekIP7jZGOeN6CvS06Rq8pxdeIPxhRZOWDSmhXe%2FwNlCcwiY31uAY6nAFVR0R9IQg80aNdGGawv64fye1ALIWwZT2IoQJrMOLuhNAz1JkLNvN1i4NOLd7YtIyuFPjeS%2BNGg0pEC0jviPAPXhD%2FT5e%2FKB9KuaGtLjdz2hSk8nIL7LBV1zM8vzY%2BiDOKSKmkFQbcfwHk1VpCbtI5lEkGyalhOWgkSOFq7jrvqqR%2FoQ49qT5NLd5aC%2BgG%2Fr%2FQE8NzLrjzZLacuDg%3D&X-Amz-SignedHeaders=host&x-id=PutObject&X-Amz-Signature=49f02640bba7ff647c839560d7b2bb261f8e66d88d5bb15351cb9b39063f3550
TOKEN=eyJhbGciOiJSUzI1NiIsImtpZCI6ImJlYW1saXQiLCJ0eXAiOiJKV1QifQ.eyJhdWQiOlsiYmVhbWxpdCJdLCJlbWFpbCI6ImRyYXBwaWVyLmNoYXJsZXNAZ21haWwuY29tIiwiZXhwIjoxNzMwMDE2MjE4LCJmYW1pbHlfbmFtZSI6IkRyYXBwaWVyIiwiZ2l2ZW5fbmFtZSI6IkNoYXJsZXMiLCJpYXQiOjE3MzAwMDkwMTgsImlzcyI6Imh0dHBzOi8vYXBpLmJlYW1saXQuZGV2L3YwIiwianRpIjoiWTFTUjFKT1FPRTNRMlVUUyIsIm5iZiI6MTczMDAwOTAxOCwic2NvcGUiOiJvZmZsaW5lX2FjY2VzcyIsInN1YiI6IjZhMmE4NDUwLTZhZGItNGViYi04M2UxLTFiN2U1YjgyMzE5MCIsInN1Yl90eXBlIjoidXNlciJ9.an4QtIHE7FXK393252LxChIxmGlSF7iT_c0abCF1ecxcDQseNX2kj1VELh6KeBhUrtYKXohNcBP7tZewvdH2kP78S5N4sOXp2daD-ug8icduwcr_i8YfDUd_ceSunrDn86yPLnkmOSY464CvE3Lo8IU11GDJjUhCrJtzUKXMncmGJ4LVGyeSN4KSEECA0bmHd79i1s1zsep9NmB-1xMnndo1Rs33i45QLf-GNW6MYCdeulMgdVbPYQoyjqD6ebch0JyLdK1YyRMsMmrw9ZjQtYg3bNgvNvWxP2xkS1LPq86VhV6AFmfgVNnSF6PhRjGp81tIuAUf0ksmtieoVRIt8xNcukDtyIz8T6yNWwnc9m3g_9GnOfKyyCkGIExdgbNMHOIuiGJkJj_HE9EGsNrUog7yA8Z_pcfkicIlU4QONnuWut27xmFWmoCLwj_DFxS1UbepdJwDDL77h8iUGB5YO_M1gMrEWyDNQN_T85JaikSr_9NCjry3dejXhSvcJr4WtJ2Njt1Epvd-7JoHCWJufCIi3BrhVJg-lNTZLyhhw4lolWTbtdsS33kKQIPi06rPrB6Qj7XrAZMtC2y0POTGopymhXcBsMA5fKuUD7-YEqMczwe4NfmYCYFD3PcIrthQ5TLAXxTllqvCNrzUYV0regzUQ4W0Z-vSJZHNIEZlBfc
activate:
	# Only here for remember, not used cause it stay in makefile
	source ~/.venv/bin/activate

setup:
	./entrypoint.sh --model-url ${MODEL_URL} --model-path tmp

setup-s3:
	./entrypoint.sh --model-url ${MODEL_S3_URL} --model-path tmp --model-protocol s3 --aws-region ${AWS_REGION} --aws-access-key-id ${AWS_ACCESS_KEY_ID} --aws-secret-access-key ${AWS_SECRET_ACCESS_KEY}

build:
	docker build -t ${DOCKER_IMAGE} .

push:
	docker build --push --platform ${PLATFORM} -t ${DOCKER_IMAGE} .
	
run:
	docker rm -f torchserve
	docker run \
		--rm \
		--name torchserve \
		-p 8080:8080 \
		-p 8081:8081 \
		${DOCKER_IMAGE} \
		--serve \
		--model-url ${MODEL_URL}

run-s3:
	docker rm -f torchserve
	docker run \
		--rm \
		--name torchserve \
		-p 8080:8080 \
		-p 8081:8081 \
		${DOCKER_IMAGE} \
		--serve \
		--model-url ${MODEL_S3_URL} \
		--model-protocol s3 \
		--aws-region ${AWS_REGION} \
		--aws-access-key-id ${AWS_ACCESS_KEY_ID} \
		--aws-secret-access-key ${AWS_SECRET_ACCESS_KEY}

test:
	curl http://127.0.0.1:8080/predictions/densenet161 -T samples/shadow.jpg
	curl http://127.0.0.1:8080/predictions/densenet161 -T samples/pixel.jpg

test-prod:
	curl --request POST \
		--url 'https://edge-gw.beamlit.net/chris/torch/predictions/densenet161' \
		-T samples/shadow.jpg \
		--header 'Authorization: Bearer ${TOKEN}'

upload-model:
	@if [ -z "$(MODEL_FILE)" ]; then \
		echo "MODEL_FILE is not set. Please provide the path to the model file."; \
		exit 1; \
	fi
	@if [ -z "$(S3_PRESIGNED_URL)" ]; then \
		echo "S3_PRESIGNED_URL is not set. Please provide the pre-signed S3 URL."; \
		exit 1; \
	fi
	curl -# -X PUT -T $(MODEL_FILE) -H "Content-Type: application/octet-stream" "$(S3_PRESIGNED_URL)"
