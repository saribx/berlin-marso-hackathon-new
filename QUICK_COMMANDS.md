# ⚡ QUICK COMMANDS - Copy & Paste

## 🎯 Current Status:
- ✅ Easy: Training now (at 37%+, will reach 80-100%)
- ⏸️ Medium: Ready to train next
- ⏸️ Hard: Ready after Medium

---

## 📋 Commands to Run (IN ORDER):

### 1. Wait for Easy to finish (~15 min remaining)
Just let it complete. You'll see:
```
100%|██████████████████████| 20000/20000 [XX:XX<00:00, XX.XXit/s]
```

---

### 2. Immediately start Medium (WITH ORGANIZER FIX):
```bash
python il/train.py method=dp_medium demo_dir=medium max_episode_steps=400
```
**Time:** 30-35 minutes
**Watch for:** sort_accuracy should reach 70-85%
**NOTE:** `max_episode_steps=400` is CRITICAL - gives robot time for 4 parcels!

---

### 3. Immediately start Hard (WITH ORGANIZER FIX):
```bash
python il/train.py method=dp_hard demo_dir=hard max_episode_steps=600
```
**Time:** 35-40 minutes
**Watch for:** sort_accuracy should reach 60-75%
**NOTE:** `max_episode_steps=600` for 6 parcels + 50% of final score!

---

### 4. (Optional) Evaluate each level:
```bash
# Easy
python eval.py difficulty=easy obs_mode=state \
    policy=warehouse_sort.il_policy:load_dp \
    checkpoint=il/baselines/diffusion_policy/runs/warehouse_state_dp_easy_v2/checkpoints/best_eval_sort_accuracy.pt

# Medium
python eval.py difficulty=medium obs_mode=state \
    policy=warehouse_sort.il_policy:load_dp \
    checkpoint=il/baselines/diffusion_policy/runs/warehouse_state_dp_medium_v2/checkpoints/best_eval_sort_accuracy.pt

# Hard
python eval.py difficulty=hard obs_mode=state \
    policy=warehouse_sort.il_policy:load_dp \
    checkpoint=il/baselines/diffusion_policy/runs/warehouse_state_dp_hard_v2/checkpoints/best_eval_sort_accuracy.pt
```

---

### 5. Final submission:
```bash
# Update submission.yaml with all three checkpoint paths (already done for Easy)
# Then commit and push
git add .
git commit -m "Final submission - Easy: XX%, Medium: XX%, Hard: XX%"
git push origin main
```

---

## 📊 What to Expect:

| Level | Time | Target Accuracy | Weight | Points |
|-------|------|-----------------|--------|--------|
| Easy | 25 min | 85-95% | 20% | 17-19% |
| Medium | 30 min | 65-75% | 30% | 19-22% |
| Hard | 35 min | 55-70% | 50% | 27-35% |
| **TOTAL** | **90 min** | - | **100%** | **63-76%** |

**A 70% final score would be very competitive!** 🏆

---

## ⚠️ Emergency Commands:

### If training crashes:
```bash
# Restart with same config
python il/train.py method=dp_medium demo_dir=medium  # or dp_hard
```

### If accuracy plateaus low:
```bash
# Stop (Ctrl+C) and add more iterations
python il/train.py method=dp_medium demo_dir=medium flags.total_iters=35000
```

### If running out of time:
**PRIORITY ORDER:**
1. Hard level (50% of score!) - get it trained even if not perfect
2. Medium level (30% of score)
3. Easy is already done!

---

## 🎯 Current Progress Tracker:

- [x] Easy training started
- [x] Config optimizations applied
- [ ] Easy training complete (~15 min)
- [ ] Medium training complete (~30 min)
- [ ] Hard training complete (~35 min)
- [ ] All checkpoints saved
- [ ] submission.yaml updated
- [ ] Final commit & push

---

**You've got this! Just follow the commands in order!** 🚀
