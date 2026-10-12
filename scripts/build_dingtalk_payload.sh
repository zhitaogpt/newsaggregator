#!/usr/bin/env bash
# 韬见 AI 日报：从报告抽今日摘要，构造钉钉 actionCard payload 并落盘留底
#
# 用法：
#   scripts/build_dingtalk_payload.sh YYYY-MM-DD <WX_URL>
#
# 行为：
#   - 读 daily_reports/YYYY-MM-DD_ai_daily_report.md 的「## 今日摘要」3 条 bullet
#   - 拼成钉钉 actionCard JSON，写到 send-logs/YYYY-MM-DD_dingtalk_<TS>.json
#   - 把文件路径打印到 stdout（供 send_dingtalk.sh 消费）
#   - 状态/调试信息走 stderr
#
# 前置条件：
#   - daily_reports/YYYY-MM-DD_ai_daily_report.md 已存在（含 ## 今日摘要）

set -euo pipefail

DATE="${1:-}"
WX_URL="${2:-}"
if [[ -z "$DATE" || -z "$WX_URL" ]]; then
  echo "Usage: $0 YYYY-MM-DD <WX_URL>" >&2
  exit 2
fi

REPO_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

MD="daily_reports/${DATE}_ai_daily_report.md"
if [[ ! -f "$MD" ]]; then
  echo "❌ 报告不存在: $MD" >&2
  exit 3
fi

mkdir -p send-logs
TS_FILE=$(date "+%Y-%m-%dT%H%M%S")
LOG_PATH="send-logs/${DATE}_dingtalk_${TS_FILE}.json"

python3 - "$MD" "$DATE" "$WX_URL" > "$LOG_PATH" <<'PY'
import json, pathlib, re, sys
md_path, date, wx_url = sys.argv[1], sys.argv[2], sys.argv[3]
md = pathlib.Path(md_path).read_text(encoding="utf-8")
bullets, in_block = [], False
for line in md.splitlines():
    s = line.strip()
    if re.match(r"^##\s+今日摘要", s):
        in_block = True; continue
    if in_block:
        if s.startswith("- "):
            bullets.append(s[2:].strip())
        elif s.startswith("#") or re.fullmatch(r"-{3,}", s):
            break
if not bullets:
    sys.stderr.write("❌ 报告里没找到 ## 今日摘要 bullet\n"); sys.exit(4)
text = (
    f"#### 📌 AI 日报 | {date}\n\n"
    f"##### 今日摘要\n\n"
    + "\n\n".join(f"**{i+1}.** {b}" for i, b in enumerate(bullets[:3]))
)
print(json.dumps({
    "msgtype": "actionCard",
    "actionCard": {
        "title": f"AI 日报 | {date}",
        "text": text,
        "btnOrientation": "0",
        "singleTitle": "📖 阅读全文",
        "singleURL": wx_url,
    }
}, ensure_ascii=False, indent=2))
PY

echo "▸ payload 留底: $LOG_PATH ($(wc -c <"$LOG_PATH" | tr -d ' ') bytes)" >&2
echo "$LOG_PATH"
