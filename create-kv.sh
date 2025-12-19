#!/bin/bash
# Скрипт для создания KV namespace через Wrangler CLI

echo "Создание KV namespace через Wrangler CLI..."
echo ""

# Установите Wrangler если его нет:
# npm install -g wrangler

# Создайте namespace
wrangler kv:namespace create "DOWNLOAD_COUNTER"

echo ""
echo "После создания namespace, вернитесь в Cloudflare Dashboard"
echo "и добавьте его в Pages проект через Settings → Functions → KV Namespace Bindings"

