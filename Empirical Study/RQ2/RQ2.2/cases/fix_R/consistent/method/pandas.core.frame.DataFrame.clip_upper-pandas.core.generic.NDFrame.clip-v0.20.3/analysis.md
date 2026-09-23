# 一、突变情况分析

- **Total**: 2699
- **替代API**: `pandas.core.generic.NDFrame.clip`
- **10% 阈值**: 269.9

## Vi-1 (v0.20.3-v1.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 2199 | 0.3143 |
| tokenBased | 1289 | 0.2353 |
| treeBased | 1658 | 0.3451 |

## Vi (v0.21.0-v1.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 2405 | 0.2275 |
| tokenBased | 2427 | 0.0935 |
| treeBased | 2448 | 0.1928 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 2199 | 2405 | -206 | false |
| tokenBased | 1289 | 2427 | -1138 | true |
| treeBased | 1658 | 2448 | -790 | true |

```json
{
  "total": 2699,
  "replacement_api": "pandas.core.generic.NDFrame.clip",
  "threshold_10pct": 269.9,
  "vi_minus_1": {
    "mapBased": {
      "rank": 2199,
      "score": 0.314259
    },
    "tokenBased": {
      "rank": 1289,
      "score": 0.235294
    },
    "treeBased": {
      "rank": 1658,
      "score": 0.345098
    }
  },
  "vi": {
    "mapBased": {
      "rank": 2405,
      "score": 0.227545
    },
    "tokenBased": {
      "rank": 2427,
      "score": 0.093458
    },
    "treeBased": {
      "rank": 2448,
      "score": 0.192825
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 2199,
      "vi_rank": 2405,
      "delta": -206,
      "exceeds_10pct": false
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 1289,
      "vi_rank": 2427,
      "delta": -1138,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 1658,
      "vi_rank": 2448,
      "delta": -790,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `pandas.core.frame.DataFrame.clip_upper/Vi-1_v0.20.3.py`
- **new**: `pandas.core.frame.DataFrame.clip_upper/Vi_v0.21.0.py`
- **+3 / -9**

```diff
--- pandas.core.frame.DataFrame.clip_upper/Vi-1_v0.20.3.py
+++ pandas.core.frame.DataFrame.clip_upper/Vi_v0.21.0.py
@@ -1,10 +1,4 @@
-    def clip_upper(self, threshold, axis=None):
+    def clip_upper(self, threshold, axis=None, inplace=False):
         
-        if np.any(isnull(threshold)):
-            raise ValueError("Cannot use an NA value as a clip threshold")
-
-        if is_scalar(threshold) and is_number(threshold):
-            return self._clip_with_scalar(None, threshold)
-
-        subset = self.le(threshold, axis=axis) | isnull(self)
-        return self.where(subset, threshold, axis=axis)
+        return self._clip_with_one_bound(threshold, method=self.le,
+                                         axis=axis, inplace=inplace)
```

```json
{
  "old_file": "pandas.core.frame.DataFrame.clip_upper/Vi-1_v0.20.3.py",
  "new_file": "pandas.core.frame.DataFrame.clip_upper/Vi_v0.21.0.py",
  "lines_added": 3,
  "lines_removed": 9
}
```
