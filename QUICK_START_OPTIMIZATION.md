# 🚀 QUICK OPTIMIZATION GUIDE - EASY LEVEL TO 100%

## Current Status
- **Accuracy:** ~37% on Easy level
- **Target:** 100% on Easy level
- **Time Available:** 2 hours
- **Strategy:** Fast iterations (<15min each)

## ⚡ ITERATION 1: Baseline (Run This First!)

### On Your H100/T4 Environment:

```bash
# Option A: Use the quick script
python quick_train_easy.py

# Option B: Manual command
python il/train.py method=dp demo_dir=easy
```

**What's optimized:**
- ✓ Reduced training to 10k iterations (was 30k)
- ✓ Increased batch size to 512 (was 256)
- ✓ Faster evaluation frequency (every 2500 steps)
- ✓ Video capture disabled for speed

**Expected time:** 5-7 minutes on H100, 10-15 minutes on T4

### After Training Completes:

```bash
# Evaluate the model
python quick_eval_easy.py
```

**What to share with Claude:**
1. Final `sort_accuracy` from training output
2. Evaluation results
3. Any error messages

---

## 🔥 ITERATION 2: If Not 100% Yet

If accuracy < 100%, run the more aggressive config:

```bash
python il/train.py method=dp_fast demo_dir=easy
```

**What's different:**
- Longer action horizon (12 vs 8) - robot plans further ahead
- Longer prediction horizon (24 vs 16) - better long-term reasoning
- Larger batch (1024) - better gradient estimates on H100
- Bigger network (128/256/512 vs 64/128/256) - more capacity
- More iterations (15k vs 10k)

**Expected time:** 8-12 minutes on H100

---

## 🎯 ITERATION 3: Nuclear Option (If Still Not 100%)

If still struggling, we'll try:
1. Generate more diverse demos
2. Increase to 20k+ iterations
3. Try different diffusion schedulers
4. Ensemble multiple checkpoints

But honestly, **Easy level should hit 100% by Iteration 2** - it's just 2 parcels in fixed positions!

---

## 📊 What to Look For

### Good Signs:
- ✅ `sort_accuracy` increasing steadily during training
- ✅ Loss decreasing smoothly
- ✅ Final eval `sort_accuracy` near 1.0 (100%)

### Bad Signs:
- ⚠️ `sort_accuracy` stuck at low values
- ⚠️ Loss not decreasing
- ⚠️ Evaluation videos show robot failing to grasp/place

---

## 🐛 Common Issues

### "Demo not found"
```bash
python il/download_demos.py
```

### "Out of memory"
Reduce batch_size in the config:
```yaml
flags:
  batch_size: 256  # or even 128
```

### "Training too slow"
You're probably on CPU. Check with:
```python
import torch
print(torch.cuda.is_available())  # Should be True
```

---

## 📁 Key Files Modified

1. **il/conf/method/dp.yaml** - Optimized baseline config
2. **il/conf/method/dp_fast.yaml** - Aggressive config for iteration 2
3. **quick_train_easy.py** - One-command training script
4. **quick_eval_easy.py** - One-command evaluation script

---

## 🎮 Next Steps After 100% Easy

Once Easy hits 100%, we'll move to Medium and Hard with similar optimizations:
- Medium: 4 parcels, jittered positions
- Hard: 6 parcels, jittered positions + swapping bins

The hard part is Hard level (50% weight!), but let's nail Easy first.

---

**Ready? Run `python quick_train_easy.py` in your H100 environment and let me know the results!** 🚀
