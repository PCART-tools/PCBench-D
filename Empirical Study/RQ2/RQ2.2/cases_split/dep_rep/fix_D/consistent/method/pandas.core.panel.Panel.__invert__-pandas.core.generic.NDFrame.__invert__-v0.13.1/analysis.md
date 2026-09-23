# 一、突变情况分析

- **Total**: 1250
- **替代API**: `pandas.core.generic.NDFrame.__invert__`
- **10% 阈值**: 125.0

## Vi-1 (v0.12.0-v0.13.1)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 311 | 0.6943 |
| tokenBased | 14 | 0.3462 |
| treeBased | 358 | 0.5588 |

## Vi (v0.12.0-v0.14.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 660 | 0.3754 |
| tokenBased | 151 | 0.2500 |
| treeBased | 571 | 0.4000 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 311 | 660 | -349 | true |
| tokenBased | 14 | 151 | -137 | true |
| treeBased | 358 | 571 | -213 | true |

```json
{
  "total": 1250,
  "replacement_api": "pandas.core.generic.NDFrame.__invert__",
  "threshold_10pct": 125.0,
  "vi_minus_1": {
    "mapBased": {
      "rank": 311,
      "score": 0.694313
    },
    "tokenBased": {
      "rank": 14,
      "score": 0.346154
    },
    "treeBased": {
      "rank": 358,
      "score": 0.558824
    }
  },
  "vi": {
    "mapBased": {
      "rank": 660,
      "score": 0.375371
    },
    "tokenBased": {
      "rank": 151,
      "score": 0.25
    },
    "treeBased": {
      "rank": 571,
      "score": 0.4
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 311,
      "vi_rank": 660,
      "delta": -349,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 14,
      "vi_rank": 151,
      "delta": -137,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 358,
      "vi_rank": 571,
      "delta": -213,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `R_candidates/Vi-1_v0.13.1/pandas.core.generic.NDFrame.__invert__.py`
- **new**: `R_candidates/Vi_v0.14.0/pandas.core.generic.NDFrame.__invert__.py`
- **+10 / -2**

```diff
--- R_candidates/Vi-1_v0.13.1/pandas.core.generic.NDFrame.__invert__.py
+++ R_candidates/Vi_v0.14.0/pandas.core.generic.NDFrame.__invert__.py
@@ -1,3 +1,11 @@
     def __invert__(self):
-        arr = operator.inv(_values_from_object(self))
-        return self._wrap_array(arr, self.axes, copy=False)
+        try:
+            arr = operator.inv(_values_from_object(self))
+            return self.__array_wrap__(arr)
+        except:
+
+
+            if not np.prod(self.shape):
+                return self
+
+            raise
```

```json
{
  "old_file": "R_candidates/Vi-1_v0.13.1/pandas.core.generic.NDFrame.__invert__.py",
  "new_file": "R_candidates/Vi_v0.14.0/pandas.core.generic.NDFrame.__invert__.py",
  "lines_added": 10,
  "lines_removed": 2
}
```
