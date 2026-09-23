# 一、突变情况分析

- **Total**: 4908
- **替代API**: `matplotlib.cm.ScalarMappable.set_cmap`
- **10% 阈值**: 490.8

## Vi-1 (v3.1.0-v3.2.2)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 1347 | 0.5358 |
| tokenBased | 16 | 0.4583 |
| treeBased | 1208 | 0.5000 |

## Vi (v3.1.0-v3.3.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 2215 | 0.4465 |
| tokenBased | 164 | 0.3438 |
| treeBased | 2164 | 0.4222 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 1347 | 2215 | -868 | true |
| tokenBased | 16 | 164 | -148 | false |
| treeBased | 1208 | 2164 | -956 | true |

```json
{
  "total": 4908,
  "replacement_api": "matplotlib.cm.ScalarMappable.set_cmap",
  "threshold_10pct": 490.8,
  "vi_minus_1": {
    "mapBased": {
      "rank": 1347,
      "score": 0.535849
    },
    "tokenBased": {
      "rank": 16,
      "score": 0.458333
    },
    "treeBased": {
      "rank": 1208,
      "score": 0.5
    }
  },
  "vi": {
    "mapBased": {
      "rank": 2215,
      "score": 0.446541
    },
    "tokenBased": {
      "rank": 164,
      "score": 0.34375
    },
    "treeBased": {
      "rank": 2164,
      "score": 0.422222
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 1347,
      "vi_rank": 2215,
      "delta": -868,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 16,
      "vi_rank": 164,
      "delta": -148,
      "exceeds_10pct": false
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 1208,
      "vi_rank": 2164,
      "delta": -956,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `R_candidates/Vi-1_v3.2.2/matplotlib.cm.ScalarMappable.set_cmap.py`
- **new**: `R_candidates/Vi_v3.3.0/matplotlib.cm.ScalarMappable.set_cmap.py`
- **+3 / -1**

```diff
--- R_candidates/Vi-1_v3.2.2/matplotlib.cm.ScalarMappable.set_cmap.py
+++ R_candidates/Vi_v3.3.0/matplotlib.cm.ScalarMappable.set_cmap.py
@@ -1,5 +1,7 @@
     def set_cmap(self, cmap):
         
+        in_init = self.cmap is None
         cmap = get_cmap(cmap)
         self.cmap = cmap
-        self.changed()
+        if not in_init:
+            self.changed()
```

```json
{
  "old_file": "R_candidates/Vi-1_v3.2.2/matplotlib.cm.ScalarMappable.set_cmap.py",
  "new_file": "R_candidates/Vi_v3.3.0/matplotlib.cm.ScalarMappable.set_cmap.py",
  "lines_added": 3,
  "lines_removed": 1
}
```
