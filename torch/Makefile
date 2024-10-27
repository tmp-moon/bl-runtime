MODEL_ID="s3://controlplane-prod-uploads/densenet161.mar"
DOCKER_IMAGE="sindar/alpha1234abcd"
PLATFORM="linux/amd64"
AWS_REGION=$(shell aws configure get region)
AWS_ACCESS_KEY_ID=$(shell aws configure get aws_access_key_id)
AWS_SECRET_ACCESS_KEY=$(shell aws configure get aws_secret_access_key)
PROD_TOKEN=eyJhbGciOiJSUzI1NiIsImtpZCI6ImJlYW1saXQiLCJ0eXAiOiJKV1QifQ.eyJhdWQiOlsiYmVhbWxpdCJdLCJlbWFpbCI6ImRyYXBwaWVyLmNoYXJsZXNAZ21haWwuY29tIiwiZXhwIjoxNzMwMDE2MjE4LCJmYW1pbHlfbmFtZSI6IkRyYXBwaWVyIiwiZ2l2ZW5fbmFtZSI6IkNoYXJsZXMiLCJpYXQiOjE3MzAwMDkwMTgsImlzcyI6Imh0dHBzOi8vYXBpLmJlYW1saXQuZGV2L3YwIiwianRpIjoiWTFTUjFKT1FPRTNRMlVUUyIsIm5iZiI6MTczMDAwOTAxOCwic2NvcGUiOiJvZmZsaW5lX2FjY2VzcyIsInN1YiI6IjZhMmE4NDUwLTZhZGItNGViYi04M2UxLTFiN2U1YjgyMzE5MCIsInN1Yl90eXBlIjoidXNlciJ9.an4QtIHE7FXK393252LxChIxmGlSF7iT_c0abCF1ecxcDQseNX2kj1VELh6KeBhUrtYKXohNcBP7tZewvdH2kP78S5N4sOXp2daD-ug8icduwcr_i8YfDUd_ceSunrDn86yPLnkmOSY464CvE3Lo8IU11GDJjUhCrJtzUKXMncmGJ4LVGyeSN4KSEECA0bmHd79i1s1zsep9NmB-1xMnndo1Rs33i45QLf-GNW6MYCdeulMgdVbPYQoyjqD6ebch0JyLdK1YyRMsMmrw9ZjQtYg3bNgvNvWxP2xkS1LPq86VhV6AFmfgVNnSF6PhRjGp81tIuAUf0ksmtieoVRIt8xNcukDtyIz8T6yNWwnc9m3g_9GnOfKyyCkGIExdgbNMHOIuiGJkJj_HE9EGsNrUog7yA8Z_pcfkicIlU4QONnuWut27xmFWmoCLwj_DFxS1UbepdJwDDL77h8iUGB5YO_M1gMrEWyDNQN_T85JaikSr_9NCjry3dejXhSvcJr4WtJ2Njt1Epvd-7JoHCWJufCIi3BrhVJg-lNTZLyhhw4lolWTbtdsS33kKQIPi06rPrB6Qj7XrAZMtC2y0POTGopymhXcBsMA5fKuUD7-YEqMczwe4NfmYCYFD3PcIrthQ5TLAXxTllqvCNrzUYV0regzUQ4W0Z-vSJZHNIEZlBfc

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
		${DOCKER_IMAGE} \
		--model-id ${MODEL_ID} \
		--aws-region ${AWS_REGION} \
		--aws-access-key-id ${AWS_ACCESS_KEY_ID} \
		--aws-secret-access-key ${AWS_SECRET_ACCESS_KEY}

test:
	curl http://127.0.0.1:80/predictions/densenet161 -T samples/shadow.jpg
	curl http://127.0.0.1:80/predictions/densenet161 -T samples/pixel.jpg

test-prod:
	curl --request POST \
		--url 'https://edge-gw.beamlit.net/chris/torch/predictions/densenet161' \
		-T samples/shadow.jpg \
		--header 'Authorization: Bearer ${PROD_TOKEN}'