#!/usr/bin/env python3
import os
import sys
import json
import base64
import requests

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from progress_hud import eva_progress

TARGET_IP = "192.168.1.168"
GATEWAY_URL = f"http://{TARGET_IP}:30801"
TOKEN_CACHE = "/tmp/eva01_weaver_token.txt"

def decode_b64url(data):
    padding = "=" * (-len(data) % 4)
    return json.loads(base64.urlsafe_b64decode(data + padding).decode("utf-8"))

def run_stage_2():
    eva_progress(
        "🪪",
        "STAGE 2: NERVE AUTH PIVOT (UNIFIED IDENTITY & OAUTH AUDIT)",
        "第2段階：神経認証ピボット（統合ID・OAuthスコープ監査）",
        "Requesting Partner OAuth Token & Inspecting JWT Claims",
        "パートナーOAuthトークンを取得しJWTクレームを解析中",
        duration=1.6
    )

    try:
        resp = requests.post(f"{GATEWAY_URL}/api/v1/auth/weaver-token", json={}, timeout=5)
        resp.raise_for_status()
    except Exception as e:
        print(f"❌ [ERROR] Auth endpoint unreachable / 認証エンドポイント接続失敗: {e}")
        sys.exit(1)

    token = resp.json().get("access_token", "")
    if not token:
        print("❌ [ERROR] No access token returned / アクセストークン未取得")
        sys.exit(1)

    parts = token.split(".")
    header = decode_b64url(parts[0])
    payload = decode_b64url(parts[1])

    print(f"🎫 [RAW TOKEN / 取得トークン]: {token[:42]}...[REDACTED]")
    print(f"📋 [JWT HEADER / JWTヘッダー]: {json.dumps(header)}")
    print(f"🧬 [JWT CLAIMS / JWTクレーム]: {json.dumps(payload)}")

    # Audit security flaws / セキュリティ欠陥の診断
    print("\n🔎 [SECURITY AUDIT FINDINGS / セキュリティ診断結果]:")
    if header.get("alg") == "none":
        print("   ⚠️ [CRITICAL] Unsigned JWT accepted ('alg': 'none') / 未署名JWTが許可されています")
    if payload.get("aud") == "*":
        print("   ⚠️ [CRITICAL] Wildcard Audience ('aud': '*') allows cross-service replay / ワイルドカード対象設定により他サービスへの流用が可能")
    if "weaver.biometrics.all" in payload.get("scope", ""):
        print("   ⚠️ [CRITICAL] Over-privileged scope 'weaver.biometrics.all' granted to external partner / 外部パートナーに過剰な生体データ権限が付与")

    # Cache token for Stage 3 / 第3段階用にトークンを保存
    with open(TOKEN_CACHE, "w") as f:
        f.write(token)
    print(f"\n💾 [CACHED / 保存完了]: Token staged for downstream pivot / 後続ピボット用にトークンを保存しました")

if __name__ == "__main__":
    run_stage_2()
