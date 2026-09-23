# 一、突变情况分析

- **Total**: 4188
- **替代API**: `transformers.trainer_tf.TFTrainer.setup_wandb`
- **10% 阈值**: 418.8

## Vi-1 (v3.0.2-v3.5.1)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 1105 | 0.5174 |
| tokenBased | 1 | 0.4912 |
| treeBased | 41 | 0.5663 |

## Vi (v3.0.2-v4.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 2 | 0.8571 |
| tokenBased | 1 | 0.6829 |
| treeBased | 1 | 0.7015 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 1105 | 2 | +1103 | true |
| tokenBased | 1 | 1 | +0 | false |
| treeBased | 41 | 1 | +40 | false |

```json
{
  "total": 4188,
  "replacement_api": "transformers.trainer_tf.TFTrainer.setup_wandb",
  "threshold_10pct": 418.8,
  "vi_minus_1": {
    "mapBased": {
      "rank": 1105,
      "score": 0.517415
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.491228
    },
    "treeBased": {
      "rank": 41,
      "score": 0.566265
    }
  },
  "vi": {
    "mapBased": {
      "rank": 2,
      "score": 0.857068
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.682927
    },
    "treeBased": {
      "rank": 1,
      "score": 0.701493
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 1105,
      "vi_rank": 2,
      "delta": 1103,
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
      "vi1_rank": 41,
      "vi_rank": 1,
      "delta": 40,
      "exceeds_10pct": false
    }
  ]
}
```

# 二、old → new Diff

- **old**: `R_candidates/Vi-1_v3.5.1/transformers.trainer_tf.TFTrainer.setup_wandb.py`
- **new**: `R_candidates/Vi_v4.0.0/transformers.trainer_tf.TFTrainer.setup_wandb.py`
- **+0 / -6**

```diff
--- R_candidates/Vi-1_v3.5.1/transformers.trainer_tf.TFTrainer.setup_wandb.py
+++ R_candidates/Vi_v4.0.0/transformers.trainer_tf.TFTrainer.setup_wandb.py
@@ -1,11 +1,5 @@
     def setup_wandb(self):
         
-        if hasattr(self, "_setup_wandb"):
-            warnings.warn(
-                "The `_setup_wandb` method is deprecated and won't be called in a future version, define `setup_wandb` in your subclass.",
-                FutureWarning,
-            )
-            return self._setup_wandb()
 
         logger.info('Automatic Weights & Biases logging enabled, to disable set os.environ["WANDB_DISABLED"] = "true"')
         combined_dict = {**self.model.config.to_dict(), **self.args.to_sanitized_dict()}
```

```json
{
  "old_file": "R_candidates/Vi-1_v3.5.1/transformers.trainer_tf.TFTrainer.setup_wandb.py",
  "new_file": "R_candidates/Vi_v4.0.0/transformers.trainer_tf.TFTrainer.setup_wandb.py",
  "lines_added": 0,
  "lines_removed": 6
}
```
