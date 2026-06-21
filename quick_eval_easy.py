#!/usr/bin/env python3
"""
Quick evaluation script for Easy level
Finds the best checkpoint and runs evaluation
"""

import subprocess
import sys
import os
import glob

print("="*80)
print("EVALUATING EASY LEVEL MODEL")
print("="*80)

# Find the best checkpoint
checkpoint_pattern = "il/baselines/diffusion_policy/runs/warehouse_state_dp_easy*/checkpoints/best_eval_sort_accuracy.pt"
checkpoints = glob.glob(checkpoint_pattern)

if not checkpoints:
    print("⚠️  No checkpoint found! Train the model first.")
    print(f"   Looking for: {checkpoint_pattern}")
    sys.exit(1)

checkpoint = checkpoints[0]
print(f"\n✓ Found checkpoint: {checkpoint}\n")

# Run evaluation
print("Running evaluation (100 episodes)...")
print("-" * 80)

cmd = [
    sys.executable, "eval.py",
    "difficulty=easy",
    "obs_mode=state",
    "policy=warehouse_sort.il_policy:load_dp",
    f"checkpoint={checkpoint}",
    "eval_config=conf/eval/default.yaml"
]

result = subprocess.run(cmd)

if result.returncode == 0:
    print("\n" + "="*80)
    print("✓ EVALUATION COMPLETE!")
    print("="*80)
    print("\nCheck the 'sort_accuracy' metric above")
    print("Target: 100% for Easy level")
    print("="*80)
else:
    print("\n⚠️  Evaluation failed!")
    sys.exit(1)
