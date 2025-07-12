# 環境変数設定ガイド

## 必要な環境変数

以下の環境変数を `.env` ファイルに設定してください：

```bash
# Django設定
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,your-ec2-ip
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://your-ec2-ip

# Discord Webhook
DISCORD_WEBHOOK_URL=your-discord-webhook-url

# Pusher設定
PUSHER_APP_ID=your-pusher-app-id
PUSHER_KEY=your-pusher-key
PUSHER_SECRET=your-pusher-secret
PUSHER_CLUSTER=ap3
```

## セットアップ手順

1. `.env.example` を `.env` にコピー
2. 各値を実際の値に置き換え
3. `.env` ファイルは **絶対にコミットしない**