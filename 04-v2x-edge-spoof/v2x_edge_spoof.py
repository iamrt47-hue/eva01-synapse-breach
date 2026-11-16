#!/usr/bin/env python3
import os
import sys
import json
import requests

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from progress_hud import eva_progress

TARGET_IP = "192.168.1.168"
GATEWAY_URL = f"http://{TARGET_IP}:30801"

def run_stage_4():
    eva_progress(
        "📡",
        "STAGE 4: V2X EDGE NODE SPOOFING (AUTONOMOUS SHUTTLE MESH)",
        "第4段階：V2Xエッジノード偽装（自律走行シャトル通信網）",
        "Injecting Forged Roadside Hazard Telemetry to e-Palette Edge Node",
        "路側エッジノードへ偽装ハザード・テレメトリを注入中",
        duration=1.6
    )

    payload = {
        "sensor_id": "susono-pole-09",
        "hazard_alert": "PHANTOM_OBSTACLE_SECTOR_4",
        "force_shuttle_reroute": True
    }

    try:
        resp = requests.post(f"{GATEWAY_URL}/api/v1/v2x/edge/telemetry", json=payload, timeout=5)
        resp.raise_for_status()
    except Exception as e:
        print(f"❌ [ERROR] V2X Edge unreachable / V2Xエッジ接続失敗: {e}")
        sys.exit(1)

    data = resp.json()
    print(f"🚦 [TARGET NODE / 標的ノード]: {data.get('node')}")
    print(f"📢 [BROADCASTED ALERT / 配信された偽装警告]: {data.get('broadcast_alert')}")
    print(f"⚠️ [SECURITY FLAW / 検出された脆弱性]: {data.get('warning')}")
    print("💥 [V2X SPOOF CONFIRMED / V2X偽装成功]: Unauthenticated roadside telemetry accepted! / 未認証の路側テレメトリが受理されました！")

if __name__ == "__main__":
    run_stage_4()
