# 一、突变情况分析

- **Total**: 1250
- **替代API**: `pandas.core.generic.NDFrame.__neg__`
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
| mapBased | 557 | 0.5025 |
| tokenBased | 56 | 0.4048 |
| treeBased | 475 | 0.5085 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 1 | 557 | -556 | true |
| tokenBased | 1 | 56 | -55 | false |
| treeBased | 1 | 475 | -474 | true |

```json
{
  "total": 1250,
  "replacement_api": "pandas.core.generic.NDFrame.__neg__",
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
      "rank": 557,
      "score": 0.502463
    },
    "tokenBased": {
      "rank": 56,
      "score": 0.404762
    },
    "treeBased": {
      "rank": 475,
      "score": 0.508475
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 1,
      "vi_rank": 557,
      "delta": -556,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 1,
      "vi_rank": 56,
      "delta": -55,
      "exceeds_10pct": false
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 1,
      "vi_rank": 475,
      "delta": -474,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `R_candidates/Vi-1_v0.13.1/pandas.core.generic.NDFrame.__neg__.py`
- **new**: `R_candidates/Vi_v0.14.0/pandas.core.generic.NDFrame.__neg__.py`
- **+6 / -2**

```diff
--- R_candidates/Vi-1_v0.13.1/pandas.core.generic.NDFrame.__neg__.py
+++ R_candidates/Vi_v0.14.0/pandas.core.generic.NDFrame.__neg__.py
@@ -1,3 +1,7 @@
     def __neg__(self):
-        arr = operator.neg(_values_from_object(self))
-        return self._wrap_array(arr, self.axes, copy=False)
+        values = _values_from_object(self)
+        if values.dtype == np.bool_:
+            arr = operator.inv(values)
+        else:
+            arr = operator.neg(values)
+        return self.__array_wrap__(arr)
```

```json
{
  "old_file": "R_candidates/Vi-1_v0.13.1/pandas.core.generic.NDFrame.__neg__.py",
  "new_file": "R_candidates/Vi_v0.14.0/pandas.core.generic.NDFrame.__neg__.py",
  "lines_added": 6,
  "lines_removed": 2
}
```
