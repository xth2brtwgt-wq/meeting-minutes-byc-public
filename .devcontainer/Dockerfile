# Dockerfileの例
# Pythonのベースイメージ（土台）を指定
FROM python:3.10-slim

# 作業ディレクトリを設定
WORKDIR /app

# 必要なPythonライブラリをインストール
# pandasなど、使いたいライブラリをここに記述
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ローカルPCのコードをコンテナ内の/appにコピー
COPY . .