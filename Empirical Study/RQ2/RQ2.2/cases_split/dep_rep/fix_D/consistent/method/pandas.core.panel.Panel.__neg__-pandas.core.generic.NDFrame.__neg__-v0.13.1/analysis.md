# 一、突变情况分析

- **Total**: 1250
- **替代API**: `pandas.core.generic.NDFrame.__neg__`
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
| mapBased | 582 | 0.4246 |
| tokenBased | 258 | 0.2250 |
| treeBased | 620 | 0.3750 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 311 | 582 | -271 | true |
| tokenBased | 14 | 258 | -244 | true |
| treeBased | 358 | 620 | -262 | true |

```json
{
  "total": 1250,
  "replacement_api": "pandas.core.generic.NDFrame.__neg__",
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
      "rank": 582,
      "score": 0.424638
    },
    "tokenBased": {
      "rank": 258,
      "score": 0.225
    },
    "treeBased": {
      "rank": 620,
      "score": 0.375
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 311,
      "vi_rank": 582,
      "delta": -271,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 14,
      "vi_rank": 258,
      "delta": -244,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 358,
      "vi_rank": 620,
      "delta": -262,
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
