#!/usr/bin/env bash
# 韬见 AI 日报：把已经构造好的 payload JSON 文件发送到钉钉机器人
#
# 用法：
#   scripts/send_dingtalk.sh <payload_file>
#
# 必需环境变量（必须在 shell 环境或 .env 中提供）：
#   DINGTALK_WEBHOOK_TOKEN   钉钉机器人 access_token
#   DINGTALK_WEBHOOK_SECRET  钉钉机器人加签密钥（SECxxxx）
#
# 典型联用：
#   PAYLOAD=$(scripts/build_dingtalk_payload.sh 2026-05-28 https://mp.weixin.qq.com/s/xxx)
#   scripts/send_dingtalk.sh "$PAYLOAD"

set -euo pipefail

PAYLOAD_FILE="${1:-}"
if [[ -z "$PAYLOAD_FILE" ]]; then
  echo "Usage: $0 <payload_file>" >&2
  exit 2
fi
if [[ ! -f "$PAYLOAD_FILE" ]]; then
  echo "❌ payload 文件不存在: $PAYLOAD_FILE" >&2
  exit 3
fi

REPO_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

if [[ -f .env ]]; then
  set -a
  # shellcheck disable=SC1091
  source .env
  set +a
fi

if [[ -z "${DINGTALK_WEBHOOK_TOKEN:-}" || -z "${DINGTALK_WEBHOOK_SECRET:-}" ]]; then
  echo "❌ 缺少 DINGTALK_WEBHOOK_TOKEN 或 DINGTALK_WEBHOOK_SECRET" >&2
  echo "   请在 .env 或 shell 环境中导出这两个变量" >&2
  exit 6
fi

# 加签
TIMESTAMP=$(($(date +%s) * 1000))
STRING_TO_SIGN="${TIMESTAMP}\n${DINGTALK_WEBHOOK_SECRET}"
SIGN=$(echo -ne "${STRING_TO_SIGN}" \
  | openssl dgst -sha256 -hmac "${DINGTALK_WEBHOOK_SECRET}" -binary \
  | base64 \
  | python3 -c "import sys,urllib.parse;print(urllib.parse.quote(sys.stdin.read().strip()))")
WEBHOOK="https://oapi.dingtalk.com/robot/send?access_token=${DINGTALK_WEBHOOK_TOKEN}&timestamp=${TIMESTAMP}&sign=${SIGN}"

echo "▸ 发送 → token=${DINGTALK_WEBHOOK_TOKEN:0:8}… payload=$PAYLOAD_FILE"
RESP=$(curl -s -X POST "$WEBHOOK" \
  -H "Content-Type: application/json; charset=utf-8" \
  --data-binary "@${PAYLOAD_FILE}" \
  --max-time 15)
echo "▸ resp: $RESP"

if echo "$RESP" | grep -q '"errcode":0'; then
  echo "✅ 已发送钉钉"
else
  echo "❌ 钉钉返回非 0：$RESP" >&2
  exit 5
fi
