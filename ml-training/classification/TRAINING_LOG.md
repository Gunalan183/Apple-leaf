# Augmented Model Training Log

**Started**: 2026-11-17 10:39:00  
**Dataset**: Apple_Augmented (2,417 training images)  
**Model**: DenseNet121  
**Target**: Match or exceed baseline 95.04% accuracy

---

## Training Progress

### Epoch 1 (Completed at 11:12)
- **Validation Accuracy**: 69.38%
- **Validation Loss**: 0.8140
- **Status**: ✅ Learning started
- **Notes**: Lower initial accuracy expected with augmented dataset

### Monitoring Status
- Process ID: 23160
- Runtime: 31+ minutes
- Memory: Stable
- Status: RUNNING

---

## Expected Timeline

- **Per epoch**: ~15-20 minutes
- **Total epochs**: Up to 50 (with early stopping)
- **Expected completion**: 2-3 hours from start
- **Next check**: Every 30 minutes

---

## Baseline Comparison

| Metric | Baseline (Original) | Augmented (Current) |
|--------|---------------------|---------------------|
| Dataset Size | 1,210 images | 2,417 images |
| Epoch 1 Val Acc | 86.05% | 69.38% |
| Final Test Acc | 95.04% | TBD |

---

**Last Updated**: 2026-11-17 11:15
