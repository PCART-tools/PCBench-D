# 一、突变情况分析

- **Total**: 4918
- **替代API**: `matplotlib.cm.ScalarMappable.set_norm`
- **10% 阈值**: 491.8

## Vi-1 (v3.1.0-v3.1.3)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 1577 | 0.4982 |
| tokenBased | 58 | 0.3929 |
| treeBased | 1930 | 0.4500 |

## Vi (v3.1.0-v3.2.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 2218 | 0.4537 |
| tokenBased | 248 | 0.2973 |
| treeBased | 2034 | 0.4400 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 1577 | 2218 | -641 | true |
| tokenBased | 58 | 248 | -190 | false |
| treeBased | 1930 | 2034 | -104 | false |

```json
{
  "total": 4918,
  "replacement_api": "matplotlib.cm.ScalarMappable.set_norm",
  "threshold_10pct": 491.8,
  "vi_minus_1": {
    "mapBased": {
      "rank": 1577,
      "score": 0.498246
    },
    "tokenBased": {
      "rank": 58,
      "score": 0.392857
    },
    "treeBased": {
      "rank": 1930,
      "score": 0.45
    }
  },
  "vi": {
    "mapBased": {
      "rank": 2218,
      "score": 0.453674
    },
    "tokenBased": {
      "rank": 248,
      "score": 0.297297
    },
    "treeBased": {
      "rank": 2034,
      "score": 0.44
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 1577,
      "vi_rank": 2218,
      "delta": -641,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 58,
      "vi_rank": 248,
      "delta": -190,
      "exceeds_10pct": false
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 1930,
      "vi_rank": 2034,
      "delta": -104,
      "exceeds_10pct": false
    }
  ]
}
```

# 二、old → new Diff

- **old**: `R_candidates/Vi-1_v3.1.3/matplotlib.cm.ScalarMappable.set_norm.py`
- **new**: `R_candidates/Vi_v3.2.0/matplotlib.cm.ScalarMappable.set_norm.py`
- **+1 / -0**

```diff
--- R_candidates/Vi-1_v3.1.3/matplotlib.cm.ScalarMappable.set_norm.py
+++ R_candidates/Vi_v3.2.0/matplotlib.cm.ScalarMappable.set_norm.py
@@ -1,5 +1,6 @@
     def set_norm(self, norm):
         
+        cbook._check_isinstance((colors.Normalize, None), norm=norm)
         if norm is None:
             norm = colors.Normalize()
         self.norm = norm
```

```json
{
  "old_file": "R_candidates/Vi-1_v3.1.3/matplotlib.cm.ScalarMappable.set_norm.py",
  "new_file": "R_candidates/Vi_v3.2.0/matplotlib.cm.ScalarMappable.set_norm.py",
  "lines_added": 1,
  "lines_removed": 0
}
```
