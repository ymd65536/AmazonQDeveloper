import os
import boto3
import json


def create_embedding(
        input_text: str,
        model_id: str = "amazon.titan-embed-text-v2:0"):
    """
    Create an embedding using the Amazon Bedrock model.
    Returns:
        dict: A dictionary containing the embedding and input text token count.
    """
    client = boto3.client('bedrock-runtime', region_name='us-west-2')

    native_request = {"inputText": input_text}
    request = json.dumps(native_request)

    response = client.invoke_model(modelId=model_id, body=request)
    model_response = json.loads(response["body"].read())

    return {
        "embedding": model_response["embedding"],
        "inputTextTokenCount": model_response["inputTextTokenCount"]
    }


def create_index(bucket_name: str = ''):
    client = boto3.client('s3vectors', region_name='us-west-2')

    if not bucket_name:
        bucket_name = os.environ.get(
            'S3_VECTOR_BUCKET_NAME', 's3-vector-bucket')

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
    except Exception as e:
        print("Index already exists or another error occurred.")
        print(f"Error: {e}")

    return result


if __name__ == "__main__":
    print(f"boto3 version:{boto3.__version__}")
    print("Starting S3 Vector setup...")
    create_index(os.environ.get('S3_VECTOR_BUCKET_NAME', 's3-vector-bucket'))

    print("Creating embedding for sample text...")
    sample_texts = [
        "Star Wars: A farm boy joins rebels to fight an evil empire in space",
        "Jurassic Park: Scientists create dinosaurs in a theme park that goes wrong",
        "Finding Nemo: A father fish searches the ocean to find his lost son"
    ]

    embedding_results = []
    for sample_text in sample_texts:
        embedding_result = create_embedding(sample_text)
        embedding_results.append(embedding_result['embedding'])

    s3_vectors = boto3.client('s3vectors', region_name='us-west-2')

    print("Uploading embeddings to S3 Vector index...")
    s3_vectors.put_vectors(
        vectorBucketName=os.environ.get(
            'S3_VECTOR_BUCKET_NAME', 's3-vector-bucket'),
        indexName='sample-index',
        vectors=[
            {"key": "v1", "data": {"float32": embedding_results[0]}, "metadata": {
                "id": "key1", "source_text": sample_texts[0], "genre": "scifi"}}
        ]
    )

    query_text = "List the movies about adventures in space"
    request = json.dumps({"inputText": query_text})

    bedrock = boto3.client("bedrock-runtime", region_name="us-west-2")
    response = bedrock.invoke_model(
        modelId='amazon.titan-embed-text-v2:0',
        body=request
    )

    model_response = json.loads(response["body"].read())
    embedding = model_response["embedding"]

    query_response = s3_vectors.query_vectors(
        vectorBucketName=os.environ.get(
            'S3_VECTOR_BUCKET_NAME', 's3-vector-bucket'),
        indexName='sample-index',
        queryVector={"float32": embedding},
        topK=3,
        filter={"genre": "scifi"},
        returnDistance=True,
        returnMetadata=True
    )
    results = query_response["vectors"]
    print(results)
    print("Done.")
