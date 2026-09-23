# 一、突变情况分析

- **Total**: 4257
- **替代API**: `transformers.trainer.Trainer.is_local_process_zero`
- **10% 阈值**: 425.7

## Vi-1 (v3.0.2-v4.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 1 | 0.9363 |
| tokenBased | 1 | 0.8286 |
| treeBased | 1 | 0.9821 |

## Vi (v3.1.0-v4.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 679 | 0.5827 |
| tokenBased | 1 | 0.5000 |
| treeBased | 406 | 0.5556 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 1 | 679 | -678 | true |
| tokenBased | 1 | 1 | +0 | false |
| treeBased | 1 | 406 | -405 | false |

```json
{
  "total": 4257,
  "replacement_api": "transformers.trainer.Trainer.is_local_process_zero",
  "threshold_10pct": 425.7,
  "vi_minus_1": {
    "mapBased": {
      "rank": 1,
      "score": 0.93633
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.828571
    },
    "treeBased": {
      "rank": 1,
      "score": 0.982143
    }
  },
  "vi": {
    "mapBased": {
      "rank": 679,
      "score": 0.582677
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.5
    },
    "treeBased": {
      "rank": 406,
      "score": 0.555556
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 1,
      "vi_rank": 679,
      "delta": -678,
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
      "vi1_rank": 1,
      "vi_rank": 406,
      "delta": -405,
      "exceeds_10pct": false
    }
  ]
}
```

# 二、old → new Diff

- **old**: `transformers.trainer.Trainer.is_local_master/Vi-1_v3.0.2.py`
- **new**: `transformers.trainer.Trainer.is_local_master/Vi_v3.1.0.py`
- **+3 / -4**

```diff
--- transformers.trainer.Trainer.is_local_master/Vi-1_v3.0.2.py
+++ transformers.trainer.Trainer.is_local_master/Vi_v3.1.0.py
@@ -1,5 +1,4 @@
     def is_local_master(self) -> bool:
-        if is_torch_tpu_available():
-            return xm.is_master_ordinal(local=True)
-        else:
-            return self.args.local_rank in [-1, 0]
+        
+        warnings.warn("This method is deprecated, use `Trainer.is_local_process_zero()` instead.", FutureWarning)
+        return self.is_local_process_zero()
```

```json
{
  "old_file": "transformers.trainer.Trainer.is_local_master/Vi-1_v3.0.2.py",
  "new_file": "transformers.trainer.Trainer.is_local_master/Vi_v3.1.0.py",
  "lines_added": 3,
  "lines_removed": 4
}
```
