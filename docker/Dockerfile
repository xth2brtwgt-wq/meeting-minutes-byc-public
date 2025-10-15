# Python 3.11 ベースイメージ
FROM python:3.11-slim

# 作業ディレクトリを設定
WORKDIR /app

# システムパッケージの更新と必要なツールのインストール
RUN apt-get update && apt-get install -y \
    ffmpeg \
    git \
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Pythonの依存関係をインストール
COPY meeting-minutes/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# プロジェクトファイルをコピー
COPY . .

# 必要なディレクトリを作成
RUN mkdir -p /tmp/uploads /tmp/transcripts

# ポート5000を公開
EXPOSE 5000

# 環境変数を設定
ENV FLASK_APP=meeting-minutes/app/app.py
ENV FLASK_ENV=production
ENV PYTHONPATH=/app

# アプリケーションを起動
CMD ["python", "meeting-minutes/app/app.py"]

