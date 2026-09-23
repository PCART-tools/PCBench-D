# 一、突变情况分析

- **Total**: 4908
- **替代API**: `matplotlib.cm.ScalarMappable.set_norm`
- **10% 阈值**: 490.8

## Vi-1 (v3.1.0-v3.2.2)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 2220 | 0.4537 |
| tokenBased | 248 | 0.2973 |
| treeBased | 2035 | 0.4400 |

## Vi (v3.1.0-v3.3.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 2626 | 0.3880 |
| tokenBased | 428 | 0.2444 |
| treeBased | 2721 | 0.3607 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 2220 | 2626 | -406 | false |
| tokenBased | 248 | 428 | -180 | false |
| treeBased | 2035 | 2721 | -686 | true |

```json
{
  "total": 4908,
  "replacement_api": "matplotlib.cm.ScalarMappable.set_norm",
  "threshold_10pct": 490.8,
  "vi_minus_1": {
    "mapBased": {
      "rank": 2220,
      "score": 0.453674
    },
    "tokenBased": {
      "rank": 248,
      "score": 0.297297
    },
    "treeBased": {
      "rank": 2035,
      "score": 0.44
    }
  },
  "vi": {
    "mapBased": {
      "rank": 2626,
      "score": 0.387978
    },
    "tokenBased": {
      "rank": 428,
      "score": 0.244444
    },
    "treeBased": {
      "rank": 2721,
      "score": 0.360656
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 2220,
      "vi_rank": 2626,
      "delta": -406,
      "exceeds_10pct": false
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 248,
      "vi_rank": 428,
      "delta": -180,
      "exceeds_10pct": false
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 2035,
      "vi_rank": 2721,
      "delta": -686,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `R_candidates/Vi-1_v3.2.2/matplotlib.cm.ScalarMappable.set_norm.py`
- **new**: `R_candidates/Vi_v3.3.0/matplotlib.cm.ScalarMappable.set_norm.py`
- **+3 / -1**

```diff
--- R_candidates/Vi-1_v3.2.2/matplotlib.cm.ScalarMappable.set_norm.py
+++ R_candidates/Vi_v3.3.0/matplotlib.cm.ScalarMappable.set_norm.py
@@ -1,7 +1,9 @@
     def set_norm(self, norm):
         
         cbook._check_isinstance((colors.Normalize, None), norm=norm)
+        in_init = self.norm is None
         if norm is None:
             norm = colors.Normalize()
         self.norm = norm
-        self.changed()
+        if not in_init:
+            self.changed()
```

```json
{
  "old_file": "R_candidates/Vi-1_v3.2.2/matplotlib.cm.ScalarMappable.set_norm.py",
  "new_file": "R_candidates/Vi_v3.3.0/matplotlib.cm.ScalarMappable.set_norm.py",
  "lines_added": 3,
  "lines_removed": 1
}
```
