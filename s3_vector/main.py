import os
import boto3
import json


def main():
    print(f"boto3 version:{boto3.__version__}")
    client = boto3.client('bedrock-runtime', region_name='us-west-2')

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


def create_index(bucket_name: str = ''):
    client = boto3.client('s3vectors', region_name='us-west-2')

    if not bucket_name:
        bucket_name = os.environ.get('S3_VECTOR_BUCKET_NAME', 's3-vector-bucket')

    result = None
    try:
        result = client.create_index(
            vectorBucketName=bucket_name,
            indexName='sample-index',
            dataType='float32',
            dimension=1024,
            distanceMetric='cosine'
        )
        print(f"Index created successfully in bucket: {bucket_name}")
    except:
        print(f"Index already exists or another error occurred.")

    return result

if __name__ == "__main__":
    print("Starting S3 Vector setup...")
    create_index(os.environ.get('S3_VECTOR_BUCKET_NAME', 's3-vector-bucket'))
    print("Done.")
