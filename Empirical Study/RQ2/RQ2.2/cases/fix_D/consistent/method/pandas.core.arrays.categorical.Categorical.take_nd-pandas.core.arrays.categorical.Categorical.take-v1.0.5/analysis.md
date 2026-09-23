# 一、突变情况分析

- **Total**: 584
- **替代API**: `pandas.core.arrays.categorical.Categorical.take`
- **10% 阈值**: 58.4

## Vi-1 (v0.25.3-v1.0.5)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 1 | 0.5658 |
| tokenBased | 1 | 0.7103 |
| treeBased | 1 | 0.8300 |

## Vi (v0.25.3-v1.1.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 253 | 0.3135 |
| tokenBased | 303 | 0.1875 |
| treeBased | 316 | 0.2847 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 1 | 253 | -252 | true |
| tokenBased | 1 | 303 | -302 | true |
| treeBased | 1 | 316 | -315 | true |

```json
{
  "total": 584,
  "replacement_api": "pandas.core.arrays.categorical.Categorical.take",
  "threshold_10pct": 58.4,
  "vi_minus_1": {
    "mapBased": {
      "rank": 1,
      "score": 0.565789
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.71028
    },
    "treeBased": {
      "rank": 1,
      "score": 0.83
    }
  },
  "vi": {
    "mapBased": {
      "rank": 253,
      "score": 0.313529
    },
    "tokenBased": {
      "rank": 303,
      "score": 0.1875
    },
    "treeBased": {
      "rank": 316,
      "score": 0.284672
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 1,
      "vi_rank": 253,
      "delta": -252,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 1,
      "vi_rank": 303,
      "delta": -302,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 1,
      "vi_rank": 316,
      "delta": -315,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `R_candidates/Vi-1_v1.0.5/pandas.core.arrays.categorical.Categorical.take.py`
- **new**: `R_candidates/Vi_v1.1.0/pandas.core.arrays.categorical.Categorical.take.py`
- **+4 / -21**

```diff
--- R_candidates/Vi-1_v1.0.5/pandas.core.arrays.categorical.Categorical.take.py
+++ R_candidates/Vi_v1.1.0/pandas.core.arrays.categorical.Categorical.take.py
@@ -1,22 +1,5 @@
-    def take(self, indexer, allow_fill: bool = False, fill_value=None):
+    def take(self: _T, indexer, allow_fill: bool = False, fill_value=None) -> _T:
         
-        indexer = np.asarray(indexer, dtype=np.intp)
-
-        dtype = self.dtype
-
-        if isna(fill_value):
-            fill_value = -1
-        elif allow_fill:
-
-            if fill_value in self.categories:
-                fill_value = self.categories.get_loc(fill_value)
-            else:
-                msg = (
-                    f"'fill_value' ('{fill_value}') is not in this "
-                    "Categorical's categories."
-                )
-                raise TypeError(msg)
-
-        codes = take(self._codes, indexer, allow_fill=allow_fill, fill_value=fill_value)
-        result = type(self).from_codes(codes, dtype=dtype)
-        return result
+        return NDArrayBackedExtensionArray.take(
+            self, indexer, allow_fill=allow_fill, fill_value=fill_value
+        )
```

```json
{
  "old_file": "R_candidates/Vi-1_v1.0.5/pandas.core.arrays.categorical.Categorical.take.py",
  "new_file": "R_candidates/Vi_v1.1.0/pandas.core.arrays.categorical.Categorical.take.py",
  "lines_added": 4,
  "lines_removed": 21
}
```
