import os
from s3_vector_engine import core

if __name__ == "__main__":
    print("Query S3 Vector index...")
    query_text = "List the movies about adventures in space"
    embedding_query_text = core.create_embedding_query_text(query_text)

    query_response = core.query_vectors(
        bucket_name=os.environ.get(
            'S3_VECTOR_BUCKET_NAME', 's3-vector-bucket'),
        index_name='sample-index',
        query_vector={"float32": embedding_query_text},
        top_k=3,
        filter={"genre": "scifi"},
        return_distance=True,
        return_metadata=True
    )

    results = query_response["vectors"]

    print(results[0]["metadata"]["source_text"])
    print("Done.")
