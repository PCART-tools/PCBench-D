# 一、突变情况分析

- **Total**: 4257
- **替代API**: `transformers.trainer.Trainer.is_world_process_zero`
- **10% 阈值**: 425.7

## Vi-1 (v3.0.2-v4.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 1 | 1.0000 |
| tokenBased | 1 | 0.8537 |
| treeBased | 1 | 0.9853 |

## Vi (v3.1.0-v4.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 679 | 0.5827 |
| tokenBased | 2 | 0.4318 |
| treeBased | 1664 | 0.4902 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 1 | 679 | -678 | true |
| tokenBased | 1 | 2 | -1 | false |
| treeBased | 1 | 1664 | -1663 | true |

```json
{
  "total": 4257,
  "replacement_api": "transformers.trainer.Trainer.is_world_process_zero",
  "threshold_10pct": 425.7,
  "vi_minus_1": {
    "mapBased": {
      "rank": 1,
      "score": 1.0
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.853659
    },
    "treeBased": {
      "rank": 1,
      "score": 0.985294
    }
  },
  "vi": {
    "mapBased": {
      "rank": 679,
      "score": 0.582677
    },
    "tokenBased": {
      "rank": 2,
      "score": 0.431818
    },
    "treeBased": {
      "rank": 1664,
      "score": 0.490196
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
      "vi_rank": 2,
      "delta": -1,
      "exceeds_10pct": false
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 1,
      "vi_rank": 1664,
      "delta": -1663,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `transformers.trainer.Trainer.is_world_master/Vi-1_v3.0.2.py`
- **new**: `transformers.trainer.Trainer.is_world_master/Vi_v3.1.0.py`
- **+2 / -4**

```diff
--- transformers.trainer.Trainer.is_world_master/Vi-1_v3.0.2.py
+++ transformers.trainer.Trainer.is_world_master/Vi_v3.1.0.py
@@ -1,6 +1,4 @@
     def is_world_master(self) -> bool:
         
-        if is_torch_tpu_available():
-            return xm.is_master_ordinal(local=False)
-        else:
-            return self.args.local_rank == -1 or torch.distributed.get_rank() == 0
+        warnings.warn("This method is deprecated, use `Trainer.is_world_process_zero()` instead.", FutureWarning)
+        return self.is_world_process_zero()
```

```json
{
  "old_file": "transformers.trainer.Trainer.is_world_master/Vi-1_v3.0.2.py",
  "new_file": "transformers.trainer.Trainer.is_world_master/Vi_v3.1.0.py",
  "lines_added": 2,
  "lines_removed": 4
}
```
