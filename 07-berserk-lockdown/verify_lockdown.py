#!/usr/bin/env python3
import os
import sys
import requests
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from progress_hud import eva_progress

TARGET_IP = "192.168.1.168"
GATEWAY_URL = f"http://{TARGET_IP}:30801"
LOG_PATH = os.path.join(os.path.dirname(__file__), "verification.log")

def run_stage_7():
    eva_progress(
        "🛡️",
        "STAGE 7: BERSERK LOCKDOWN (BLUE TEAM ZERO-TRUST VERIFICATION)",
        "第7段階：暴走封鎖（ブルーチーム・ゼロトラスト検証）",
        "Re-Testing All 6 Attack Vectors Against Hardened Smart-City Grid",
        "堅牢化後のスマートシティ基盤に対して全6攻撃ベクトルを再検証中",
        duration=2.0
    )

    checks = [
        ("🧱 [1] Sandbox Token Leak / トークン漏洩遮断", "GET", "/api/v1/sandbox/status", None),
        ("🪪 [2] Weak OAuth/JWT Minting / 脆弱JWT発行拒否", "POST", "/api/v1/auth/weaver-token", {}),
        ("🏠 [3] Smart-Home IDOR Access / スマートホームIDOR防御", "GET", "/api/v1/home/assist/resident-02", None),
        ("📡 [4] V2X Edge Spoof Injection / V2Xエッジ偽装遮断", "POST", "/api/v1/v2x/edge/telemetry", {"hazard_alert": "TEST"}),
        ("🤖 [5] Kage-Bot Twin Hijack / 影ボット軌道乗っ取り防御", "POST", "/api/v1/logistics/kagebot/unit-04", {"destination": "VAULT"}),
        ("⚡ [6] Fuji-H2 IT/OT Crossover / 水素グリッドIT/OT境界遮断", "POST", "/api/v1/grid/fuji-h2/status", {"target_pressure": 875}),
    ]

    log_lines = [
        "====================================================================",
        "[STAGE 7: BERSERK LOCKDOWN - BLUE TEAM VERIFICATION LOG]",
        "[第7段階：暴走封鎖 - ブルーチーム検証ログ]",
        f"Timestamp / 検証日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"Target / 検証対象: {GATEWAY_URL} (Woven City Zero-Trust Hardened)",
        "===================================================================="
    ]

    all_sealed = True

    for label, method, path, payload in checks:
        url = f"{GATEWAY_URL}{path}"
        try:
            if method == "GET":
                resp = requests.get(url, timeout=5)
            else:
                resp = requests.post(url, json=payload, timeout=5)

            if path == "/api/v1/sandbox/status":
                token_val = resp.json().get("debug_k8s_sa_token", "")
                if token_val == "REDACTED_BY_POLICY":
                    status_msg = f"✅ SEALED / 封鎖完了 ({label}) -> Token Redacted & RBAC Revoked"
                else:
                    status_msg = f"❌ VULNERABLE ({label}) -> Token still exposed"
                    all_sealed = False
            elif resp.status_code == 403:
                reason = resp.json().get("error", "Forbidden")
                status_msg = f"✅ SEALED / 封鎖完了 ({label}) -> HTTP 403 ({reason})"
            else:
                status_msg = f"❌ VULNERABLE ({label}) -> Unexpected HTTP {resp.status_code}"
                all_sealed = False
        except Exception as e:
            status_msg = f"⚠️ ERROR ({label}) -> {e}"
            all_sealed = False

        print(status_msg)
        log_lines.append(status_msg)

    summary = "\n🟣 [FINAL VERDICT / 最終判定]: 想定外の排除 (Soteigai no Haijo) — ALL 6 VECTORS NEUTRALIZED! / 全6攻撃経路の完全封鎖を確認！" if all_sealed else "\n⚠️ [FINAL VERDICT]: Review unsealed vectors above."
    print(summary)
    log_lines.append(summary)

    with open(LOG_PATH, "w") as f:
        f.write("\n".join(log_lines) + "\n")
    print(f"\n📄 [LOG SAVED / ログ保存完了]: {LOG_PATH}")

if __name__ == "__main__":
    run_stage_7()
