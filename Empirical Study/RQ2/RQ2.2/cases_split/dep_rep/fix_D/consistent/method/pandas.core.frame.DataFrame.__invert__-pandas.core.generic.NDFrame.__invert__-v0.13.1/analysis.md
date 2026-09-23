# 一、突变情况分析

- **Total**: 1250
- **替代API**: `pandas.core.generic.NDFrame.__invert__`
- **10% 阈值**: 125.0

## Vi-1 (v0.12.0-v0.13.1)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 1 | 1.0000 |
| tokenBased | 1 | 0.8000 |
| treeBased | 1 | 0.9556 |

## Vi (v0.12.0-v0.14.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 506 | 0.5327 |
| tokenBased | 4 | 0.4865 |
| treeBased | 41 | 0.6250 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 1 | 506 | -505 | true |
| tokenBased | 1 | 4 | -3 | false |
| treeBased | 1 | 41 | -40 | false |

```json
{
  "total": 1250,
  "replacement_api": "pandas.core.generic.NDFrame.__invert__",
  "threshold_10pct": 125.0,
  "vi_minus_1": {
    "mapBased": {
      "rank": 1,
      "score": 1.0
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.8
    },
    "treeBased": {
      "rank": 1,
      "score": 0.955556
    }
  },
  "vi": {
    "mapBased": {
      "rank": 506,
      "score": 0.532663
    },
    "tokenBased": {
      "rank": 4,
      "score": 0.486486
    },
    "treeBased": {
      "rank": 41,
      "score": 0.625
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 1,
      "vi_rank": 506,
      "delta": -505,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 1,
      "vi_rank": 4,
      "delta": -3,
      "exceeds_10pct": false
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 1,
      "vi_rank": 41,
      "delta": -40,
      "exceeds_10pct": false
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
