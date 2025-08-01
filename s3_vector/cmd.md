# S3 VectorsをAWS CLIで使う

## Setup

デフォルトリージョンを変更します。

```bash
export AWS_DEFAULT_REGION=us-west-2
```

バケット名にアカウントIDを含めるため、AWSアカウントIDを取得します。

```bash
export AWS_ACCOUNT_ID=`aws sts get-caller-identity --query "Account" --output text` && echo $AWS_ACCOUNT_ID
```

## コマンド一覧

S3 VectorsをAWS CLIで操作するためのコマンド一覧です。

ベクターバケットを作成します。

```bash
aws s3vectors create-vector-bucket --vector-bucket-name my-vector-${AWS_ACCOUNT_ID}
```

```bash
export S3_VECTOR_BUCKET_NAME=my-vector-${AWS_ACCOUNT_ID}
```

ベクターバケットの一覧を表示します。

```bash
aws s3vectors list-vector-buckets
```

ベクターバケット名のみを取得します。

```bash
aws s3vectors list-vector-buckets --query "vectorBuckets[0].vectorBucketName" --output text
```

ベクターバケットを削除します。

```bash
aws s3vectors delete-vector-bucket --vector-bucket-name my-vector-${AWS_ACCOUNT_ID}
```
