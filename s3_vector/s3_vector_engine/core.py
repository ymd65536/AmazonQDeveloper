import os
import json
import boto3


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


def create_embedding_sample_text(texts: list,
                                 model_id: str = "amazon.titan-embed-text-v2:0"):
    """
    Create embeddings for a list of texts using the specified model.
    Returns:
        list: A list of dictionaries containing embeddings and input text token counts.
    """

    client = boto3.client('bedrock-runtime', region_name='us-west-2')
    embeddings = []
    for text in texts:
        native_request = {"inputText": text}
        request = json.dumps(native_request)

        response = client.invoke_model(modelId=model_id, body=request)
        model_response = json.loads(response["body"].read())

        embeddings.append(model_response["embedding"])
    return embeddings


def create_embedding_query_text(
        query_text: str,
        model_id: str = "amazon.titan-embed-text-v2:0"):
    """
    Create an embedding for a query text using the specified model.
    Returns:
        dict: A dictionary containing the embedding.
    """
    client = boto3.client('bedrock-runtime', region_name='us-west-2')

    native_request = {"inputText": query_text}
    request = json.dumps(native_request)

    response = client.invoke_model(modelId=model_id, body=request)
    model_response = json.loads(response["body"].read())

    return model_response["embedding"]


def query_vectors(
        bucket_name: str,
        index_name: str,
        query_vector: dict,
        top_k: int = 3,
        filter: dict = None,
        return_distance: bool = True,
        return_metadata: bool = True):
    """
    Query vectors from the S3 Vector index.
    """
    s3_vectors = boto3.client('s3vectors', region_name='us-west-2')

    response = s3_vectors.query_vectors(
        vectorBucketName=bucket_name,
        indexName=index_name,
        queryVector=query_vector,
        topK=top_k,
        filter=filter,
        returnDistance=return_distance,
        returnMetadata=return_metadata
    )

    return response


def put_vectors(
        bucket_name: str,
        index_name: str,
        vectors: list):
    """
    Upload vectors to the S3 Vector index.
    """
    s3_vectors = boto3.client('s3vectors', region_name='us-west-2')

    try:
        s3_vectors.put_vectors(
            vectorBucketName=bucket_name,
            indexName=index_name,
            vectors=vectors
        )
        print("Vectors uploaded successfully.")
    except Exception as e:
        print(f"Error uploading vectors: {e}")