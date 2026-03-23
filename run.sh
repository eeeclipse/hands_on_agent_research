#!/usr/bin/env bash
# Research Digest Agent 실행 스크립트
# 사용법: ./run.sh [옵션]
#   --profile NAME   phd 또는 industry (기본: phd)
#   --dry-run        API 키 없이 수집+랭킹만 테스트
#   --days N         최근 N일 수집 (기본: 7)
#   --threshold F    관련성 임계값 (기본: 0.35)

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# .env 로드
if [ -f "$SCRIPT_DIR/.env" ]; then
  export $(grep -v '^#' "$SCRIPT_DIR/.env" | xargs)
fi

uv run "$SCRIPT_DIR/agent.py" "$@"
