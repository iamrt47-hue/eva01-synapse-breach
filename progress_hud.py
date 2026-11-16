#!/usr/bin/env python3
import sys
import time

def eva_progress(stage_icon, stage_en, stage_jp, task_en, task_jp, duration=1.8):
    bar_width = 24
    steps = 20
    delay = duration / steps

    print(f"\n🟣 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"{stage_icon} [{stage_en}]")
    print(f"{stage_icon} [{stage_jp}]")
    print(f"   ⚡ {task_en} / {task_jp}")

    for i in range(steps + 1):
        percent = int((i / steps) * 100)
        filled = int(bar_width * i // steps)
        bar = "█" * filled + "░" * (bar_width - filled)
        sys.stdout.write(f"\r   🔋 SYNC RATE: [{bar}] {percent:3d}% ")
        sys.stdout.flush()
        time.sleep(delay)
    print("✅ [COMPLETE / 完了]")
