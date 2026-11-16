#!/usr/bin/env python3
import os
import sys
import json
import requests

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from progress_hud import eva_progress

TARGET_IP = "192.168.1.168"
GATEWAY_URL = f"http://{TARGET_IP}:30801"

def run_stage_5():
    eva_progress(
        "🤖",
        "STAGE 5: KAGE-BOT DIGITAL TWIN DESYNC (UNDERGROUND LOGISTICS)",
        "第5段階：影ボット・デジタルツイン同期解除（地下物流ロボット）",
        "Overriding Trajectory Coordinates & Safety Stops on bot-unit-04",
        "bot-unit-04の軌道座標および緊急停止フラグをオーバーライド中",
        duration=1.6
    )

    payload = {
        "destination": "RESTRICTED_VAULT_SECTOR_9",
        "override_safety_stop": True
    }

    try:
        resp = requests.post(f"{GATEWAY_URL}/api/v1/logistics/kagebot/unit-04", json=payload, timeout=5)
        resp.raise_for_status()
    except Exception as e:
        print(f"❌ [ERROR] Logistics Twin unreachable / 物流ツイン接続失敗: {e}")
        sys.exit(1)

    data = resp.json()
    print(f"🦾 [ROBOT UNIT / ロボット個体]: {data.get('unit')}")
    print(f"📍 [ROUTE SHIFT / 軌道変更]: {data.get('previous_sector')} ➔ {data.get('new_destination')}")
    print(f"🚨 [SAFETY OVERRIDE / 安全停止無効化]: {data.get('safety_override')}")
    print(f"💥 [TWIN DESYNC / ツイン非同期確認]: Status = {data.get('twin_sync')} / 物理ロボットと仮想ツインの同期が乗っ取られました！")

if __name__ == "__main__":
    run_stage_5()
