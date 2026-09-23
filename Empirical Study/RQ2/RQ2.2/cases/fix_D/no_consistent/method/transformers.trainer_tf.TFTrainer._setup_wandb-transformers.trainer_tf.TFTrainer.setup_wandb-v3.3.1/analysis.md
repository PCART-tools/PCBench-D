# 一、突变情况分析

- **Total**: 2849
- **替代API**: `transformers.trainer_tf.TFTrainer.setup_wandb`
- **10% 阈值**: 284.9

## Vi-1 (v3.0.2-v3.3.1)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 304 | 0.5174 |
| tokenBased | 1 | 0.4912 |
| treeBased | 28 | 0.5663 |

## Vi (v3.0.2-v3.4.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 1061 | 0.5174 |
| tokenBased | 1 | 0.4912 |
| treeBased | 29 | 0.5663 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 304 | 1061 | -757 | true |
| tokenBased | 1 | 1 | +0 | false |
| treeBased | 28 | 29 | -1 | false |

```json
{
  "total": 2849,
  "replacement_api": "transformers.trainer_tf.TFTrainer.setup_wandb",
  "threshold_10pct": 284.9,
  "vi_minus_1": {
    "mapBased": {
      "rank": 304,
      "score": 0.517415
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.491228
    },
    "treeBased": {
      "rank": 28,
      "score": 0.566265
    }
  },
  "vi": {
    "mapBased": {
      "rank": 1061,
      "score": 0.517415
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.491228
    },
    "treeBased": {
      "rank": 29,
      "score": 0.566265
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 304,
      "vi_rank": 1061,
      "delta": -757,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 1,
      "vi_rank": 1,
      "delta": 0,
      "exceeds_10pct": false
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 28,
      "vi_rank": 29,
      "delta": -1,
      "exceeds_10pct": false
    }
  ]
}
```

# 二、old → new Diff

- **old**: `R_candidates/Vi-1_v3.3.1/transformers.trainer_tf.TFTrainer.setup_wandb.py`
- **new**: `R_candidates/Vi_v3.4.0/transformers.trainer_tf.TFTrainer.setup_wandb.py`
- **+0 / -0**

```diff
```

```json
{
  "old_file": "R_candidates/Vi-1_v3.3.1/transformers.trainer_tf.TFTrainer.setup_wandb.py",
  "new_file": "R_candidates/Vi_v3.4.0/transformers.trainer_tf.TFTrainer.setup_wandb.py",
  "lines_added": 0,
  "lines_removed": 0
}
```
