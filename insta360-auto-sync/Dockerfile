# Insta360自動同期システム - Dockerイメージ定義
FROM alpine:latest

# メタデータ
LABEL maintainer="Yoshi"
LABEL description="Insta360自動同期システム"
LABEL version="1.0.0"

# 必要なパッケージをインストール
RUN apk add --no-cache \
    python3 \
    py3-pip \
    cifs-utils \
    gcc \
    python3-dev \
    musl-dev \
    linux-headers \
    bash \
    curl \
    tzdata \
    && ln -sf /usr/share/zoneinfo/Asia/Tokyo /etc/localtime \
    && echo "Asia/Tokyo" > /etc/timezone

# Pythonパッケージのインストール
COPY requirements.txt /tmp/
RUN pip3 install --no-cache-dir --break-system-packages -r /tmp/requirements.txt

# 作業ディレクトリの設定
WORKDIR /app

# アプリケーションファイルをコピー
COPY scripts/ /app/scripts/
COPY utils/ /app/utils/
COPY config/ /app/config/

# ログディレクトリの作成
RUN mkdir -p /app/logs

# 実行権限の設定
RUN chmod +x /app/scripts/*.py /app/scripts/*.sh

# 環境変数の設定
ENV PYTHONPATH=/app
ENV TZ=Asia/Tokyo

# ヘルスチェック
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python3 /app/scripts/test_connection.py || exit 1

# デフォルトコマンド
CMD ["python3", "/app/scripts/run_scheduler.py"]
