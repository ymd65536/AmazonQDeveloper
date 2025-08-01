
## この記事で伝えたいこと（ポイント）

## はじめに

この記事では「この前リリースされた機能って実際に動かすとどんな感じなんだろう」とか「もしかしたら内容次第では使えるかも？？」などAWSサービスの中でも特定の機能にフォーカスして検証していく記事です。主な内容としては実践したときのメモを中心に書きます。（忘れやすいことなど）
誤りなどがあれば書き直していく予定です。

今回はAWS Summit NYCでも紹介があったAmazon S3 Vectors（以下、本文ではS3 Vectors）を検証します。

参考：[ベクトルの保存とクエリをネイティブにサポートする最初のクラウドオブジェクトストレージ、Amazon S3 Vectors (プレビュー版) を発表
](https://aws.amazon.com/jp/about-aws/whats-new/2025/07/amazon-s3-vectors-preview-native-support-storing-querying-vectors/)

参考：[ニューヨークで開催される 2025 年の AWS Summit に関する主要なお知らせ](https://aws.amazon.com/jp/blogs/news/top-announcements-of-the-aws-summit-in-new-york-2025/)

参考：[Introducing Amazon S3 Vectors: First cloud storage with native vector support at scale (preview)](https://aws.amazon.com/jp/blogs/aws/introducing-amazon-s3-vectors-first-cloud-storage-with-native-vector-support-at-scale/)

## Amazon S3 Vectorsとは

S3 Vectorsは簡単に説明するとAmazon S3にベクトルデータを保存するための新しい機能です。
公式サイトでは以下のように説明されています。

※翻訳した内容です

> Amazon S3 Vectorsは、ベクトルを保存およびクエリするためのネイティブサポートを備えた最初のクラウドオブジェクトストアであり、AIエージェント、AI推論、およびAmazon S3に保存されたコンテンツのセマンティック検索のための目的に応じたコスト最適化されたベクトルストレージを提供します。アップロード、保存、およびクエリのコストを最大90％削減することで、S3 Vectorsは大規模なベクトルデータセットを作成および使用することをコスト効果的にし、AIエージェントのメモリとコンテキスト、およびS3データのセマンティック検索結果を改善します。Amazon S3と同じ弾力性、スケール、および耐久性を提供するように設計されており、数十億のベクトルを保存し、サブ秒クエリパフォーマンスでデータを検索できます。大規模なベクトルインデックスを構築および維持する必要があるアプリケーションに最適であり、大量の情報を整理および検索できます。

参考：[What is S3 Vectors? - AWS公式サイト](https://aws.amazon.com/jp/s3/features/vectors/)

ベクトルを保存？大規模なベクトルインデックスを構築？コンテンツのセマンティック検索のための目的に応じた...なんだって？
よくわからないですね。1つずつ見ていきましょう。

### ベクトル（ベクター）とは

S3 Vectorsを知るためには、ベクトルとは何かを理解する必要があります。
まず、ベクトルという言葉を聞いて数学や物理学に理解のある人は矢印を思い浮かべるかもしれません。

ベクトルは大きさと方向を持つ量でたとえば、物理学では力や速度を表すのに使われます。
地球に住むすべての人類は重力という力を受けていますが、これもベクトルで表現できます。

なお、向きを持たない量はスカラーと呼ばれ、たとえば温度や質量などが該当します。
ちなみにプログラミング言語にScalaというJVM言語がありますが、これはイタリア語の「階段」が語源であるため、ベクトルとは関係ありません。

そして、AIや機械学習の世界ではデータを数値のリストとして表現することが一般的でこれを「ベクトル」と呼びます。

たとえば

- 画像をベクトル化すると、画像の特徴を数値で表現
- テキストをベクトル化すると、単語や文の意味を数値で表現

といった具合です。このベクトルを保存するためのストレージ（ベクターストアあるいはベクターデータベース）がS3 Vectorsです。

### 余談：次元数ってなんぞ

ベクトルを扱っていると次元数という言葉に遭遇します。次元数というのは要するに「表現の粒度」のことだと考えていただければと思います。

次元数（機械学習の分野では特徴量）が多いほど表現の幅が広がりますが、「次元の呪い」という難問にぶつかります。これは主成分分析（PCA）や特徴量選択によって改善が期待できます。

次元数、生成AIに入力されたデータから抽出された特徴量はより抽象化されたベクトルとして表現されます。この抽象化されたベクトルが存在する空間を「潜在空間」と呼び、そのベクトルを「潜在表現」と呼びます。

## ベクターストア(ベクターデータベース)とは

ベクターストアは、ベクトルデータを効率的に保存、検索、管理するためのデータベースです。
ベクターデータベースと表現される場合もありますが、基本的には同じ意味です。

ただし、ベクターデータベースと表現した場合はデータベースサービスであることを強調する場合が多いです。
※たとえば、元はデータベースサービスとして提供していたが、ベクトル保存もできるようになった場合などはベクターデータベースと表現されることが多いです。

ちなみにAWSにおいて、ベクターデータベースとして提供されているサービスがいくつかあります。

- Amazon Aurora for PostgreSQLとAmazon RDS for PostgreSQL
  - pgvectorを使ってベクトルデータを保存できる
- Amazon Neptune ML
  - GraphRAGが実現できる
- Amazon MemoryDB
  - MemoryDBベースのベクターデータベース
- Amazon DocumentDB (MongoDB 互換)
  - Amazon SageMaker Canvasと組みわせてノーコード機械学習が可能

[ベクターデータベースとは ベクターデータベースの説明 - AWS](https://aws.amazon.com/jp/what-is/vector-databases/)

## で、S3にベクトルデータが入ると何が嬉しいの

S3 Vectorsが「ベクトルデータを保存できるベクターストアの機能」であるということがわかったところでS3 Vectorsを使うと何が嬉しいのでしょうか。
ひとことで言うと「オブジェクトストレージベースでベクトル検索ができるようになる」というところです。

具体的には以下のとおりです。

- ベクトル検索用のDBが必要であり、オブジェクトストレージにあるデータをお手軽にRAGできなかった
  - Knowledge base for Amazon BedrockとOpenSearchを組み合わせる方法がありますが、コストは比較的に高め
- RDBやNoSQL系のマネージドサービスを使う必要がある
  - ちょっとしたベクトル検索をするためにRDBやNoSQL系のマネージドサービスを使うのはオーバースペック※
- オブジェクトストレージとAWS SDKでベクトル検索ができるようになる

※ちょっとしたベクトル検索ではPineconeやFAISSなどのベクターデータベースを使うこともあります。Pineconeに至ってはAWSで利用できるためおすすめです。

## 前提条件（利用サービスとツール）

今回はS3 Vectorsを使って、ベクトルデータを検索する基本的なハンズオンを行います。
なお、今回はAWS SDK for Python (Boto3)を使って簡単に実装していきますが

あくまでも検証のためなので、実際のアプリケーションでは別の構成を検討することをおすすめします。

また、最近になってAWS ToolkitによるAWS Lambdaの編集が可能になりました。
今回はこの機能を使ってサーバレスの開発を進めます。

参考:[Introducing an enhanced local IDE experience for AWS Lambda developers](https://aws.amazon.com/jp/blogs/compute/introducing-an-enhanced-local-ide-experience-for-aws-lambda-developers/)

（※[日本語版](https://aws.amazon.com/jp/blogs/news/simplify-serverless-development-with-console-to-ide-and-remote-debugging-for-aws-lambda/)）

なお、S3 Vectorsはコンソールでは実行できない操作があるため、AWS CLIを利用します。以上を踏まえて利用サービスとツールは以下のとおりです。

利用サービス

- Amazon S3 Vectors
- Amazon Bedrock
  - Titan Text Embeddings V2とTitan Embeddings G1 - Textを利用
- AWS Lambda
  - ランタイムはPython3を利用

利用ツール

- AWS CLI
  - aws-cli/2.27.63 Python/3.13.5 Darwin/24.5.0 source/arm64
- AWS Toolkit for Visual Studio Code
  - [リンク](https://docs.aws.amazon.com/ja_jp/toolkit-for-vscode/latest/userguide/welcome.html)
- AWS SDK for Python
  - version 1.40.0

### 大まかな流れ

- S3 Vectorsのベクターバケットを作成する
- Lambdaの実行ロールを作成
- Lambdaの作成
- ベクターバケットにデータを格納
- 実行
- AWS ToolkitでLambdaを修正する

## ハンズオン

### S3 Vectorsのベクターバケットを作成する

まずはデフォルトリージョンをS3 Vecotorsに対応しているリージョンに変更します。

```bash
export AWS_DEFAULT_REGION=us-west-2
```

バケット名にアカウントIDを含めるため、AWSアカウントIDを取得します。

```bash
export AWS_ACCOUNT_ID=`aws sts get-caller-identity --query "Account" --output text` && echo $AWS_ACCOUNT_ID
```

ベクターバケットを作成します。

```bash
aws s3vectors create-vector-bucket --vector-bucket-name my-vector-${AWS_ACCOUNT_ID}
```

```bash
export S3_VECTOR_BUCKET_NAME=my-vector-${AWS_ACCOUNT_ID}
```

ベクターバケット名のみを取得します。

```bash
aws s3vectors list-vector-buckets --query "vectorBuckets[0].vectorBucketName" --output text
```

### ベクターバケットにデータを格納

AWS SDKでやります。

### Lambdaと実行ロールの作成

todo: 執筆時点におけるLambdaは"boto3 version:1.38.36"であるため、boto3のバージョンを上げるために専用のレイヤーを作成します。

AWS CDKでやります。

## おまけ：AWSでイイ感じのリモート開発環境を構築して優勝する

ハンズオンは以上ですが、さらにイイ感じの開発環境で今回のハンズオンを実践していく話を書きます。（書きたいだけです）
具体的にはAmazon CodeCatalystでビッグウェーブを作り、Amazon Q Developerでバイブスを上げるという話です。Amazon フォーーーーーーーーー！！！！！！

### AWS ToolkitでLambdaを修正する

※AWS CDKでデプロイしたLambdaはAWS Toolkitではなく、AWS CDKで修正したほうが良いですが、今回はお試し

## 片付け方法

S3 VectorsのバケットはS3バケット同様に中身がある場合は削除できません。

## まとめ
