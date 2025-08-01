import os
from s3_vector_engine import core

if __name__ == "__main__":
    print("Starting S3 Vector setup...")
    core.create_index(os.environ.get('S3_VECTOR_BUCKET_NAME', 's3-vector-bucket'))

    print("Creating embedding for sample text...")
    sample_texts = [
        "Star Wars: A farm boy joins rebels to fight an evil empire in space",
        "Jurassic Park: Scientists create dinosaurs in a theme park that goes wrong"
    ]

    embedding_results = core.create_embedding_sample_text(sample_texts)

    """
    Upload vectors to the S3 Vector index.
    """
    print("Uploading embeddings to S3 Vector index...")

    vectors = [
        {"key": "v1", "data": {"float32": embedding_results[0]}, "metadata": {
            "id": "key1", "source_text": sample_texts[0], "genre": "scifi"}},
        {"key": "v2", "data": {"float32": embedding_results[1]}, "metadata": {
            "id": "key2", "source_text": sample_texts[1], "genre": "scifi"}}
    ]

    core.put_vectors(
        bucket_name=os.environ.get(
            'S3_VECTOR_BUCKET_NAME', 's3-vector-bucket'),
        index_name='sample-index',
        vectors=vectors
    )
