# ✅ Hackathon Checklist - Path to Victory

## 📋 Easy Level (Target: 100%)

### Iteration 1 (NOW - 5-7 min on H100)
- [ ] Run `python quick_train_easy.py` on Lightning AI/Colab
- [ ] Check final `sort_accuracy` in output
- [ ] Run `python quick_eval_easy.py` for full evaluation
- [ ] **Decision Point:**
  - ✅ If accuracy ≥ 95%: Move to Medium level
  - ⚠️ If accuracy < 95%: Go to Iteration 2

### Iteration 2 (If needed - 8-10 min on H100)
- [ ] Run `python il/train.py method=dp_fast demo_dir=easy`
- [ ] Evaluate with adjusted hyperparameters
- [ ] **Decision Point:**
  - ✅ If accuracy ≥ 95%: Move to Medium level
  - ⚠️ If still struggling: Share logs with Claude for debugging

---

## 📋 Medium Level (Target: >80%)

### Preparation
- [ ] Create `il/conf/method/dp_medium.yaml` (based on dp_fast)
- [ ] Adjust: `total_iters=20000`, `pred_horizon=32`
- [ ] Generate/download medium demos

### Training (15-20 min on H100)
- [ ] Run `python il/train.py method=dp_medium demo_dir=medium`
- [ ] Monitor `sort_accuracy` during training
- [ ] Target: >80% accuracy

### Optimization (if needed)
- [ ] Increase network capacity: `unet_dims=[256, 512, 1024]`
- [ ] Train longer: 30k iterations
- [ ] Check for grasping/placing failure modes in videos

---

## 📋 Hard Level (Target: >70%, THIS IS 50% OF YOUR SCORE!)

### Preparation
- [ ] Create `il/conf/method/dp_hard.yaml` (most aggressive)
- [ ] Critical settings:
  - `total_iters=30000` (longer episodes, more complexity)
  - `pred_horizon=40` (6 parcels = long-horizon task)
  - `unet_dims=[256, 512, 1024]` (maximum capacity)
  - `batch_size=1024` (if GPU memory allows)

### Training (20-30 min on H100)
- [ ] Run `python il/train.py method=dp_hard demo_dir=hard`
- [ ] **Key challenge:** Bins swap positions between episodes
- [ ] Robot must read colors, not memorize positions
- [ ] Monitor for bin confusion in eval videos

### Advanced Optimizations (if time allows)
- [ ] Generate extra demos (300+ instead of 200)
- [ ] Data augmentation (swap bin positions in training data)
- [ ] Ensemble multiple checkpoints
- [ ] Increase inference steps: `num_inference_steps=32`

---

## 📋 Final Submission

### Before Submitting
- [ ] Verify all checkpoints exist:
  - `warehouse_state_dp_easy/checkpoints/best_eval_sort_accuracy.pt`
  - `warehouse_state_dp_medium/checkpoints/best_eval_sort_accuracy.pt`
  - `warehouse_state_dp_hard/checkpoints/best_eval_sort_accuracy.pt`

- [ ] Update `submission.yaml` with correct checkpoint paths

- [ ] Test each level one final time:
  ```bash
  python eval.py difficulty=easy obs_mode=state \
      policy=warehouse_sort.il_policy:load_dp \
      checkpoint=<easy_checkpoint>

  # Repeat for medium and hard
  ```

- [ ] Calculate final weighted score:
  ```
  final_score = 0.2 × easy_acc + 0.3 × medium_acc + 0.5 × hard_acc
  ```

- [ ] Commit and push to GitHub:
  ```bash
  git add .
  git commit -m "Optimized state diffusion policy - <YOUR_SCORE>% final score"
  git push origin main
  ```

- [ ] Submit GitHub URL to competition

---

## ⏱️ Time Management (2 hours total)

| Phase | Time Budget | Status |
|-------|-------------|--------|
| Easy Level | 20 min | ⏳ In progress |
| Medium Level | 30 min | ⏸️ Pending |
| Hard Level | 50 min | ⏸️ Pending |
| Testing & Submission | 20 min | ⏸️ Pending |

---

## 🎯 Score Targets

| Level | Weight | Current | Target | Optimistic |
|-------|--------|---------|--------|------------|
| Easy | 20% | 37% | 95% | 100% |
| Medium | 30% | ??? | 70% | 85% |
| Hard | 50% | ??? | 60% | 75% |
| **FINAL** | **100%** | **~37%** | **65%** | **80%+** |

A 65% final score would be competitive. 75%+ would be very strong. 80%+ would likely win!

---

## 🚨 If Something Goes Wrong

### Training crashes / OOM
- Reduce `batch_size` to 256 or 128
- Reduce `unet_dims` to [64, 128, 256]

### Accuracy plateaus early
- Train longer (increase `total_iters`)
- Larger network (increase `unet_dims`)
- More demos (generate extra with `il/gen_demos.py`)

### Robot behavior looks weird
- Check evaluation videos
- Common issues:
  - Grasping failures: Increase `obs_horizon`
  - Placing failures: Increase `pred_horizon`
  - Slow/timeout: Increase `max_episode_steps`

### Out of time
- **Priority order:**
  1. Hard level (50% weight!) - get to 60%+ minimum
  2. Medium level (30% weight) - get to 70%+
  3. Easy level (20% weight) - already at 37%

A score of 40% Easy + 70% Medium + 65% Hard = **60.5% final** is still decent!

---

**NOW GO RUN THAT TRAINING! Time is ticking! ⏰**
