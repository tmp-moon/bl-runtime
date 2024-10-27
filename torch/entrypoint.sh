#!/bin/bash

# Initialize variables
MODEL_URL=$MODEL_URL
MODEL_NAME=${MODEL_NAME:-model.mar}
MODEL_PATH=${MODEL_PATH:-/home/model-server}
MODEL_PROTOCOL=${MODEL_PROTOCOL:-https}
AWS_REGION=$AWS_REGION
AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
SERVE=${SERVE:-false}


parse_arguments()
{
    # Parse arguments
    while [[ "$#" -gt 0 ]]; do
        case $1 in
            --model-url) MODEL_URL="$2"; shift 2 ;;
            --serve) SERVE="true"; shift ;;
            --model-path) MODEL_PATH="$2"; shift 2 ;;
            --model-name) MODEL_NAME="$2"; shift 2 ;;
            --model-protocol) MODEL_PROTOCOL="$2"; shift 2 ;;
            --aws-region) AWS_REGION="$2"; shift 2 ;;
            --aws-access-key-id) AWS_ACCESS_KEY_ID="$2"; shift 2 ;;
            --aws-secret-access-key) AWS_SECRET_ACCESS_KEY="$2"; shift 2 ;;
            *) echo "Unknown parameter passed: $1"; exit 1 ;;
        esac
    done

    # Check if model_url argument is provided
    if [ -z "$MODEL_URL" ]; then
        echo "Usage: $0 --model-url <model_url> [--model-name <model_name>] [--aws-region <aws_region>] [--aws-access-key-id <aws_access_key_id>] [--aws-secret-access-key <aws_secret_access_key>]"
        exit 1
    fi
}

download_http()
{
    if [ ! -f "$MODEL_PATH/model-store/$MODEL_NAME" ]; then
        echo "Downloading model from $MODEL_URL to $MODEL_PATH/model-store/$MODEL_NAME"
        curl -L -o "$MODEL_PATH/model-store/$MODEL_NAME" "$MODEL_URL"
    else
        echo "File $MODEL_PATH/model-store/$MODEL_NAME already exists. Skipping download."
    fi
}

download_s3()
{
    echo "Downloading model from $MODEL_URL to $MODEL_PATH/model-store/$MODEL_NAME"
    if ! AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY aws s3 cp "$MODEL_URL" "$MODEL_PATH/model-store/$MODEL_NAME" \
        --region "$AWS_REGION"; then
        echo "Failed to download model from S3. Exiting."
        exit 1
    fi
}

download_model()
{
    mkdir -p "$MODEL_PATH/model-store"
    if [ "$MODEL_PROTOCOL" == "https" ]; then
        download_http
    elif [ "$MODEL_PROTOCOL" == "http" ]; then
        download_http
    elif [ "$MODEL_PROTOCOL" == "s3" ]; then
        download_s3
    else
        echo "Unsupported protocol: $MODEL_PROTOCOL"
        exit 1
    fi
}

generate_config_properties()
{
    echo "Generating config.properties file"
    cat <<EOL > "$MODEL_PATH/config.properties"
inference_address=http://0.0.0.0:8080
management_address=http://0.0.0.0:8081
model_store=$MODEL_PATH/model-store
load_models=${MODEL_NAME}
disable_token_authorization=true
EOL
}


function start_torchserve()
{
    echo "Starting TorchServe..."
    torchserve --model-store "$MODEL_PATH/model-store" --ts-config "$MODEL_PATH/config.properties"
    tail -f /dev/null
}

parse_arguments "$@"
download_model
generate_config_properties

if [ "$SERVE" == "true" ]; then
    start_torchserve
fi

