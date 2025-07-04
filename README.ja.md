# aisandbox

Codex用のサンドボックスです。

## シンプルHTTPSサーバー

このリポジトリには、Pythonで実装された、RFC 7231 に準拠した軽量な HTTPS Web サーバーが含まれています。

### セットアップ

1. 依存関係をインストールします:

    ```bash
    pip install -r requirements.txt
    ```

2. 証明書と秘密鍵を生成するか、既存のものを用意してください。`server/server_config.yaml` を編集し、証明書(`certfile`)と秘密鍵(`keyfile`)のパスを設定します。

3. HTML などのリソースを `resource_path` で指定したディレクトリに置きます。`server/html` には HTML5、CSS3、JavaScript のサンプルが含まれています。

### 実行

以下のコマンドでサーバーを起動します:

```bash
python server/simple_https_server.py -c server/server_config.yaml
```

サーバーは、設定されたホストとポートで HTTPS として待ち受けます。

### ブラウザからの設定編集

サーバー起動中に `https://<ホスト>:<ポート>/config.html` にアクセスすると、
`server_config.yaml` の内容を閲覧・編集できます。`resource_path` の変更は
再起動なしで即座に反映されます。保存後はサーバーが自動的に再起動し、
その他の項目も反映されます。この再起動はこのページからの操作時のみ行われます。
各入力欄はフォーカスが外れたときに検証され、エラーがあるとボタンは無効のままです。
ポート番号などの全角数字は半角に自動変換されてから検証されます。
フィールド横の **?** アイコンにマウスを重ねると、現在の言語で簡単な説明と例が表示されます。

インデックスページと設定編集ページの右上には、日本語と英語を切り替える
トグルボタンがあります。**日本語** または **English** をクリックすると、
ページ内の表示が即座に切り替わります。選択した言語はローカルストレージに保存され、次回以降も反映されます。

### 自己署名証明書の生成（任意）

テスト用に自己署名証明書を生成する場合は、以下のコマンドを実行します:

```bash
openssl req -x509 -newkey rsa:4096 -keyout server/key.pem -out server/cert.pem -days 365 -nodes -subj "/CN=example.com"
```

### 設定項目

- `host`: サーバーをバインドするアドレス
- `port`: リッスンするポート（HTTPS の場合は通常 443）
- `domain`: 参照用のドメイン名
- `certfile`: TLS 証明書のパス
- `keyfile`: 証明書の秘密鍵のパス
- `resource_path`: 配信する静的リソースを含むディレクトリ
