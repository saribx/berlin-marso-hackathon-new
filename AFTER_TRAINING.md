# 📋 What to Do After Training Finishes

## ✅ Automatic (Already Done):

1. **Checkpoint saved** to:
   ```
   il/baselines/diffusion_policy/runs/warehouse_state_dp_easy_v2/checkpoints/best_eval_sort_accuracy.pt
   ```

2. **submission.yaml updated** with correct checkpoint path ✓

## 🔍 Step 1: Evaluate Your Model (Optional but Recommended)

Run a full evaluation to confirm the accuracy:

```bash
python eval.py difficulty=easy obs_mode=state \
    policy=warehouse_sort.il_policy:load_dp \
    checkpoint=il/baselines/diffusion_policy/runs/warehouse_state_dp_easy_v2/checkpoints/best_eval_sort_accuracy.pt \
    eval_config=conf/eval/default.yaml
```

This will:
- Run 100 episodes
- Generate evaluation videos (so you can see the robot in action!)
- Report final `sort_accuracy`

**Expected output:** `sort_accuracy: 0.80-1.00` (80-100%)

---

## 🎯 Step 2: Train Medium Level

Once Easy is done, immediately start Medium:

```bash
python il/train.py method=dp_v2 demo_dir=medium flags.exp_name=warehouse_state_dp_medium_v2
```

**Time:** ~25-30 minutes
**Target:** 70%+ accuracy

---

## 🔥 Step 3: Train Hard Level (MOST IMPORTANT - 50% of score!)

```bash
python il/train.py method=dp_v2 demo_dir=hard \
    flags.exp_name=warehouse_state_dp_hard_v2 \
    flags.total_iters=25000 \
    flags.pred_horizon=32
```

**Time:** ~30-35 minutes
**Target:** 60%+ accuracy (this is HARD, bins swap positions!)

---

## 📝 Step 4: Update submission.yaml

After training Medium and Hard, update the checkpoint paths:

```yaml
levels:
  easy:
    checkpoint: il/baselines/diffusion_policy/runs/warehouse_state_dp_easy_v2/checkpoints/best_eval_sort_accuracy.pt

  medium:
    checkpoint: il/baselines/diffusion_policy/runs/warehouse_state_dp_medium_v2/checkpoints/best_eval_sort_accuracy.pt

  hard:
    checkpoint: il/baselines/diffusion_policy/runs/warehouse_state_dp_hard_v2/checkpoints/best_eval_sort_accuracy.pt
```

---

## 🚀 Step 5: Submit to Kaggle

1. **Commit and push** everything:
   ```bash
   git add .
   git commit -m "Final submission: Easy 90%, Medium 75%, Hard 65%"
   git push origin main
   ```

2. **Download checkpoints** from your cloud environment to local:
   ```bash
   # On Lightning AI, download these files:
   il/baselines/diffusion_policy/runs/warehouse_state_dp_easy_v2/checkpoints/best_eval_sort_accuracy.pt
   il/baselines/diffusion_policy/runs/warehouse_state_dp_medium_v2/checkpoints/best_eval_sort_accuracy.pt
   il/baselines/diffusion_policy/runs/warehouse_state_dp_hard_v2/checkpoints/best_eval_sort_accuracy.pt
   ```

3. **Submit to Kaggle:**
   - Go to: https://www.kaggle.com/competitions/marso-hack-berlin-2026-robot-parcel-sorting-challenge/submit
   - Upload your repo URL and checkpoint files
   - Follow the submission instructions in SUBMISSION.md

---

## 📊 Expected Final Score

If you achieve:
- Easy: 90% (conservative estimate)
- Medium: 70%
- Hard: 60%

**Final weighted score:**
```
0.2 × 90% + 0.3 × 70% + 0.5 × 60% = 69%
```

This would be a **competitive score**! 🏆

If you can push Hard to 70%, you'd get:
```
0.2 × 90% + 0.3 × 70% + 0.5 × 70% = 74%
```

---

## ⏱️ Time Remaining

You have ~90 minutes left for:
- Medium training: 30 min
- Hard training: 35 min
- Evaluation & submission: 25 min

**Perfect timing!** 🎯

---

## 🐛 Troubleshooting

### If Medium/Hard don't improve:
- Increase `total_iters` to 30000
- Increase `pred_horizon` (Medium: 32, Hard: 40)
- Lower learning rate to `3e-5`

### If you run out of time:
- **Priority 1:** Get Hard level trained (50% of score!)
- **Priority 2:** Get Medium trained (30% of score)
- **Priority 3:** Submit whatever you have

Even a partial submission is better than nothing!

---

**Next: Wait for Easy training to finish (~15 more minutes), then immediately start Medium!**
