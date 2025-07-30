import boto3
import json


def main():
    print(f"boto3 version:{boto3.__version__}")
    client = boto3.client('bedrock-runtime', region_name='us-east-1')

    # Set the model ID, e.g., Titan Text Embeddings V2.
    model_id = "amazon.titan-embed-text-v2:0"

    # The text to convert to an embedding.
    input_text = "Please recommend books with a theme similar to the movie 'Inception'."

    # Create the request for the model.
    native_request = {"inputText": input_text}

    # Convert the native request to JSON.
    request = json.dumps(native_request)

    # Invoke the model with the request.
    response = client.invoke_model(modelId=model_id, body=request)

    # Decode the model's native response body.
    model_response = json.loads(response["body"].read())

    # Extract and print the generated embedding and the input text token count.
    return {
        "embedding": model_response["embedding"],
        "inputTextTokenCount": model_response["inputTextTokenCount"]
    }


def s3_vector():
    client = boto3.client('s3vectors', region_name='us-east-1')
    print(client.meta.service_model)


if __name__ == "__main__":
    s3_vector()
    print("Done.")
