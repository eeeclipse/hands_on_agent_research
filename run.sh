#!/usr/bin/env bash
# RecSys Research Agent 실행 스크립트
# 사용법: ./run.sh [옵션]
#   --dry-run        API 키 없이 수집+랭킹만 테스트
#   --days N         최근 N일 수집 (기본: 7)
#   --threshold F    관련성 임계값 (기본: 0.35)

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV="$SCRIPT_DIR/.venv"

# 가상환경이 없으면 설치 안내
if [ ! -d "$VENV" ]; then
  echo "가상환경을 먼저 생성하세요:"
  echo "  python3 -m venv .venv"
  echo "  .venv/bin/pip install -r requirements.txt"
  exit 1
fi

# .env 로드
if [ -f "$SCRIPT_DIR/.env" ]; then
  export $(grep -v '^#' "$SCRIPT_DIR/.env" | xargs)
fi

"$VENV/bin/python" "$SCRIPT_DIR/agent.py" "$@"
