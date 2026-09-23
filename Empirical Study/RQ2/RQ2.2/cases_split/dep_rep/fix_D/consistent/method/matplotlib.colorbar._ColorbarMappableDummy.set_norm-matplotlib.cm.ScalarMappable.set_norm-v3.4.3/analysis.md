# 一、突变情况分析

- **Total**: 4786
- **替代API**: `matplotlib.cm.ScalarMappable.set_norm`
- **10% 阈值**: 478.6

## Vi-1 (v3.1.0-v3.4.3)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 2653 | 0.3880 |
| tokenBased | 440 | 0.2444 |
| treeBased | 2835 | 0.3443 |

## Vi (v3.1.0-v3.5.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 55 | 0.7717 |
| tokenBased | 1 | 0.7333 |
| treeBased | 132 | 0.6000 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 2653 | 55 | +2598 | true |
| tokenBased | 440 | 1 | +439 | false |
| treeBased | 2835 | 132 | +2703 | true |

```json
{
  "total": 4786,
  "replacement_api": "matplotlib.cm.ScalarMappable.set_norm",
  "threshold_10pct": 478.6,
  "vi_minus_1": {
    "mapBased": {
      "rank": 2653,
      "score": 0.387978
    },
    "tokenBased": {
      "rank": 440,
      "score": 0.244444
    },
    "treeBased": {
      "rank": 2835,
      "score": 0.344262
    }
  },
  "vi": {
    "mapBased": {
      "rank": 55,
      "score": 0.771739
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.733333
    },
    "treeBased": {
      "rank": 132,
      "score": 0.6
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 2653,
      "vi_rank": 55,
      "delta": 2598,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 440,
      "vi_rank": 1,
      "delta": 439,
      "exceeds_10pct": false
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 2835,
      "vi_rank": 132,
      "delta": 2703,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `R_candidates/Vi-1_v3.4.3/matplotlib.cm.ScalarMappable.set_norm.py`
- **new**: `R_candidates/Vi_v3.5.0/matplotlib.cm.ScalarMappable.set_norm.py`
- **+0 / -6**

```diff
--- R_candidates/Vi-1_v3.4.3/matplotlib.cm.ScalarMappable.set_norm.py
+++ R_candidates/Vi_v3.5.0/matplotlib.cm.ScalarMappable.set_norm.py
@@ -1,9 +1,3 @@
     def set_norm(self, norm):
         
-        _api.check_isinstance((colors.Normalize, None), norm=norm)
-        in_init = self.norm is None
-        if norm is None:
-            norm = colors.Normalize()
         self.norm = norm
-        if not in_init:
-            self.changed()
```

```json
{
  "old_file": "R_candidates/Vi-1_v3.4.3/matplotlib.cm.ScalarMappable.set_norm.py",
  "new_file": "R_candidates/Vi_v3.5.0/matplotlib.cm.ScalarMappable.set_norm.py",
  "lines_added": 0,
  "lines_removed": 6
}
```
