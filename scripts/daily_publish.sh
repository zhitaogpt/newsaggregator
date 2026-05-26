#!/usr/bin/env bash
# 韬见 AI 日报：cover → HTML → git push → WeChat 草稿
#
# 用法：
#   scripts/daily_publish.sh YYYY-MM-DD
#
# 前置条件：
#   - daily_reports/YYYY-MM-DD_ai_daily_report.md 已存在（含 ## 今日摘要）
#   - .env 含 WECHAT_APPID / WECHAT_API_KEY
#   - 当前 git 工作区干净，并且 origin 可推送（GitHub 公开仓 raw URL 是 cover 来源）

set -euo pipefail

DATE="${1:-}"
if [[ -z "$DATE" ]]; then
  echo "Usage: $0 YYYY-MM-DD" >&2
  exit 2
fi

REPO_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

MD="daily_reports/${DATE}_ai_daily_report.md"
if [[ ! -f "$MD" ]]; then
  echo "❌ 报告不存在: $MD" >&2
  exit 3
fi

# 加载 .env（只取我们关心的两个 key）
if [[ -f .env ]]; then
  set -a
  # shellcheck disable=SC1091
  source .env
  set +a
fi
if [[ -z "${WECHAT_APPID:-}" || -z "${WECHAT_API_KEY:-}" ]]; then
  echo "❌ .env 缺少 WECHAT_APPID 或 WECHAT_API_KEY" >&2
  exit 4
fi

DAY_SHORT="${DATE:5:2}${DATE:8:2}"   # 0526
COVER="brand_assets/wechat_render/cover_${DAY_SHORT}.png"
HTML="brand_assets/wechat_render/v_${DAY_SHORT}.html"

# 1) 渲染封面
echo "▸ render cover → $COVER"
python3 scripts/wechat_render/cover_render.py "$MD" "$COVER"

# 2) 渲染 HTML（注入封面）
echo "▸ render html  → $HTML"
python3 scripts/wechat_render/render.py "$MD" "$HTML" --cover "$COVER"

# 3) 抽取 summary（前两条 ## 今日摘要 用 · 拼接，截到 120 字）
SUMMARY="$(python3 - "$MD" <<'PY'
import re, sys, pathlib
md = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
bullets = []
in_block = False
for line in md.splitlines():
    s = line.strip()
    if re.match(r"^##\s+今日摘要", s):
        in_block = True
        continue
    if in_block:
        if s.startswith("- "):
            bullets.append(s[2:].strip())
        elif s.startswith("#") or re.fullmatch(r"-{3,}", s) or (s == "" and bullets):
            if s.startswith("#") or re.fullmatch(r"-{3,}", s):
                break
out = " · ".join(bullets[:2])
if len(out) > 118:
    out = out[:117] + "…"
print(out)
PY
)"
echo "▸ summary: $SUMMARY"

# 4) git commit & push（cover + html）—— GitHub raw 需要这一步
echo "▸ git push 封面/HTML 到 origin"
git add "$COVER" "$HTML"
if ! git diff --cached --quiet; then
  git commit -m "daily: ${DATE} cover + html"
  git push origin HEAD
else
  echo "  (无变更，跳过 commit)"
fi

# 5) 调 wx.limyai 入草稿（清掉本机代理 — wx.limyai 经常被代理隧道拒掉）
COVER_RAW_URL="https://raw.githubusercontent.com/zhitaogpt/newsaggregator/main/${COVER}"
echo "▸ publish → WeChat 草稿 cover=${COVER_RAW_URL}"
unset http_proxy https_proxy HTTP_PROXY HTTPS_PROXY
python3 .claude/skills/wechat-article-publisher/scripts/wechat_api.py publish \
  --appid  "$WECHAT_APPID" \
  --html   "$HTML" \
  --cover  "$COVER_RAW_URL" \
  --summary "$SUMMARY" \
  --author "韬见编辑部"

echo "✅ ${DATE} 已推送到 WeChat 草稿"
