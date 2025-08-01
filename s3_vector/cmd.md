# S3 VectorsをAWS CLIで使う

## コマンド一覧

S3 VectorsをAWS CLIで操作するためのコマンド一覧です。

ベクターバケットの一覧を表示します。

```bash
aws s3vectors list-vector-buckets
```

ベクターバケット名のみを取得します。

```bash
aws s3vectors list-vector-buckets --query "vectorBuckets[0].vectorBucketName" --output text
```

```bash
aws s3vectors delete-vector-bucket --vector-bucket-name 
```
