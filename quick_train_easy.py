#!/usr/bin/env python3
"""
ITERATION 1: Fast Easy Level Training for H100
Run this in your Lightning AI / Colab environment
Expected time: 5-7 minutes on H100, 10-15 minutes on T4
"""

import subprocess
import sys
import os

print("="*80)
print("MARSO HACKATHON - EASY LEVEL OPTIMIZATION")
print("="*80)
print("\nITERATION 1: Baseline training with optimized hyperparameters")
print("- 10k iterations (reduced from 30k for speed)")
print("- Batch size 512 (2x default, optimized for H100)")
print("- Eval every 2500 steps (faster feedback)")
print("\nTarget: Get quick feedback on convergence pattern")
print("="*80 + "\n")

# Step 1: Install kagglehub if needed
demo_path = "il/demos/easy/trajectory.state.pd_ee_delta_pos.physx_cuda.h5"
if not os.path.exists(demo_path):
    print("⚠️  Demos not found! Installing kagglehub and downloading...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", "kagglehub"], check=False)
    subprocess.run([sys.executable, "il/download_demos.py"], check=True)
    print("✓ Demos downloaded\n")
else:
    print(f"✓ Demos found at {demo_path}\n")

# Step 2: Train the model
print("Starting training...")
print("-" * 80)
cmd = [
    sys.executable, "il/train.py",
    "method=dp",
    "demo_dir=easy"
]

result = subprocess.run(cmd)

if result.returncode == 0:
    print("\n" + "="*80)
    print("✓ TRAINING COMPLETE!")
    print("="*80)
    print("\nCheckpoint location:")
    print("  il/baselines/diffusion_policy/runs/warehouse_state_dp_easy/checkpoints/")
    print("\nNext steps:")
    print("  1. Check the final sort_accuracy in the output above")
    print("  2. Run evaluation: python eval.py difficulty=easy obs_mode=state \\")
    print("       policy=warehouse_sort.il_policy:load_dp \\")
    print("       checkpoint=il/baselines/diffusion_policy/runs/warehouse_state_dp_easy/checkpoints/best_eval_sort_accuracy.pt")
    print("\n  3. Share the results with Claude for next iteration!")
    print("="*80)
else:
    print("\n⚠️  Training failed! Check error messages above.")
    sys.exit(1)
