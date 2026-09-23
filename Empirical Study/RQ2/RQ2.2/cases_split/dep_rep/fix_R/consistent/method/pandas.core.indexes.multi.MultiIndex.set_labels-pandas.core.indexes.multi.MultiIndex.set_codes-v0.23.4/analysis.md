# 一、突变情况分析

- **Total**: 639
- **替代API**: `pandas.core.indexes.multi.MultiIndex.set_codes`
- **10% 阈值**: 63.9

## Vi-1 (v0.23.4-v1.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 1 | 0.9993 |
| tokenBased | 1 | 0.9310 |
| treeBased | 1 | 0.9913 |

## Vi (v0.24.0-v1.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 463 | 0.3487 |
| tokenBased | 327 | 0.2203 |
| treeBased | 353 | 0.3709 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 1 | 463 | -462 | true |
| tokenBased | 1 | 327 | -326 | true |
| treeBased | 1 | 353 | -352 | true |

```json
{
  "total": 639,
  "replacement_api": "pandas.core.indexes.multi.MultiIndex.set_codes",
  "threshold_10pct": 63.9,
  "vi_minus_1": {
    "mapBased": {
      "rank": 1,
      "score": 0.999299
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.931034
    },
    "treeBased": {
      "rank": 1,
      "score": 0.991304
    }
  },
  "vi": {
    "mapBased": {
      "rank": 463,
      "score": 0.348748
    },
    "tokenBased": {
      "rank": 327,
      "score": 0.220339
    },
    "treeBased": {
      "rank": 353,
      "score": 0.370861
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 1,
      "vi_rank": 463,
      "delta": -462,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 1,
      "vi_rank": 327,
      "delta": -326,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 1,
      "vi_rank": 353,
      "delta": -352,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `pandas.core.indexes.multi.MultiIndex.set_labels/Vi-1_v0.23.4.py`
- **new**: `pandas.core.indexes.multi.MultiIndex.set_labels/Vi_v0.24.0.py`
- **+5 / -20**

```diff
--- pandas.core.indexes.multi.MultiIndex.set_labels/Vi-1_v0.23.4.py
+++ pandas.core.indexes.multi.MultiIndex.set_labels/Vi_v0.24.0.py
@@ -1,22 +1,7 @@
     def set_labels(self, labels, level=None, inplace=False,
                    verify_integrity=True):
-        
-        if level is not None and not is_list_like(level):
-            if not is_list_like(labels):
-                raise TypeError("Labels must be list-like")
-            if is_list_like(labels[0]):
-                raise TypeError("Labels must be list-like")
-            level = [level]
-            labels = [labels]
-        elif level is None or is_list_like(level):
-            if not is_list_like(labels) or not is_list_like(labels[0]):
-                raise TypeError("Labels must be list of lists-like")
-
-        if inplace:
-            idx = self
-        else:
-            idx = self._shallow_copy()
-        idx._reset_identity()
-        idx._set_labels(labels, level=level, verify_integrity=verify_integrity)
-        if not inplace:
-            return idx
+        warnings.warn((".set_labels was deprecated in version 0.24.0. "
+                       "Use .set_codes instead."),
+                      FutureWarning, stacklevel=2)
+        return self.set_codes(codes=labels, level=level, inplace=inplace,
+                              verify_integrity=verify_integrity)
```

```json
{
  "old_file": "pandas.core.indexes.multi.MultiIndex.set_labels/Vi-1_v0.23.4.py",
  "new_file": "pandas.core.indexes.multi.MultiIndex.set_labels/Vi_v0.24.0.py",
  "lines_added": 5,
  "lines_removed": 20
}
```
