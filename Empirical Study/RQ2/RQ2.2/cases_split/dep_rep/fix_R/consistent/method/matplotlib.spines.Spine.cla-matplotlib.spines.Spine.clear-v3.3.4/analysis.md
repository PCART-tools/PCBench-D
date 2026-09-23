# 一、突变情况分析

- **Total**: 4834
- **替代API**: `matplotlib.spines.Spine.clear`
- **10% 阈值**: 483.4

## Vi-1 (v3.3.4-v3.6.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 1 | 0.9966 |
| tokenBased | 1 | 0.6364 |
| treeBased | 1 | 0.9545 |

## Vi (v3.4.0-v3.6.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 646 | 0.5684 |
| tokenBased | 103 | 0.3182 |
| treeBased | 786 | 0.5789 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 1 | 646 | -645 | true |
| tokenBased | 1 | 103 | -102 | false |
| treeBased | 1 | 786 | -785 | true |

```json
{
  "total": 4834,
  "replacement_api": "matplotlib.spines.Spine.clear",
  "threshold_10pct": 483.4,
  "vi_minus_1": {
    "mapBased": {
      "rank": 1,
      "score": 0.996555
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.636364
    },
    "treeBased": {
      "rank": 1,
      "score": 0.954545
    }
  },
  "vi": {
    "mapBased": {
      "rank": 646,
      "score": 0.568359
    },
    "tokenBased": {
      "rank": 103,
      "score": 0.318182
    },
    "treeBased": {
      "rank": 786,
      "score": 0.578947
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 1,
      "vi_rank": 646,
      "delta": -645,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 1,
      "vi_rank": 103,
      "delta": -102,
      "exceeds_10pct": false
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 1,
      "vi_rank": 786,
      "delta": -785,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `matplotlib.spines.Spine.cla/Vi-1_v3.3.4.py`
- **new**: `matplotlib.spines.Spine.cla/Vi_v3.4.0.py`
- **+2 / -4**

```diff
--- matplotlib.spines.Spine.cla/Vi-1_v3.3.4.py
+++ matplotlib.spines.Spine.cla/Vi_v3.4.0.py
@@ -1,5 +1,3 @@
+    @_api.deprecated("3.4", alternative="Spine.clear()")
     def cla(self):
-        
-        self._position = None
-        if self.axis is not None:
-            self.axis.cla()
+        self.clear()
```

```json
{
  "old_file": "matplotlib.spines.Spine.cla/Vi-1_v3.3.4.py",
  "new_file": "matplotlib.spines.Spine.cla/Vi_v3.4.0.py",
  "lines_added": 2,
  "lines_removed": 4
}
```
