# 一、突变情况分析

- **Total**: 3180
- **替代API**: `pandas.core.frame.DataFrame.shift`
- **10% 阈值**: 318.0

## Vi-1 (v1.1.5-v1.4.4)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 642 | 0.3903 |
| tokenBased | 402 | 0.3286 |
| treeBased | 783 | 0.4199 |

## Vi (v1.1.5-v1.5.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 1333 | 0.3247 |
| tokenBased | 1290 | 0.2168 |
| treeBased | 1910 | 0.3059 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 642 | 1333 | -691 | true |
| tokenBased | 402 | 1290 | -888 | true |
| treeBased | 783 | 1910 | -1127 | true |

```json
{
  "total": 3180,
  "replacement_api": "pandas.core.frame.DataFrame.shift",
  "threshold_10pct": 318.0,
  "vi_minus_1": {
    "mapBased": {
      "rank": 642,
      "score": 0.390326
    },
    "tokenBased": {
      "rank": 402,
      "score": 0.328571
    },
    "treeBased": {
      "rank": 783,
      "score": 0.419929
    }
  },
  "vi": {
    "mapBased": {
      "rank": 1333,
      "score": 0.324734
    },
    "tokenBased": {
      "rank": 1290,
      "score": 0.216763
    },
    "treeBased": {
      "rank": 1910,
      "score": 0.305882
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 642,
      "vi_rank": 1333,
      "delta": -691,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 402,
      "vi_rank": 1290,
      "delta": -888,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 783,
      "vi_rank": 1910,
      "delta": -1127,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `R_candidates/Vi-1_v1.4.4/pandas.core.frame.DataFrame.shift.py`
- **new**: `R_candidates/Vi_v1.5.0/pandas.core.frame.DataFrame.shift.py`
- **+44 / -2**

```diff
--- R_candidates/Vi-1_v1.4.4/pandas.core.frame.DataFrame.shift.py
+++ R_candidates/Vi_v1.5.0/pandas.core.frame.DataFrame.shift.py
@@ -1,10 +1,10 @@
     @doc(NDFrame.shift, klass=_shared_doc_kwargs["klass"])
     def shift(
         self,
-        periods=1,
+        periods: int = 1,
         freq: Frequency | None = None,
         axis: Axis = 0,
-        fill_value=lib.no_default,
+        fill_value: Hashable = lib.no_default,
     ) -> DataFrame:
         axis = self._get_axis_number(axis)
 
@@ -39,6 +39,48 @@
 
             result.columns = self.columns.copy()
             return result
+        elif (
+            axis == 1
+            and periods != 0
+            and fill_value is not lib.no_default
+            and ncols > 0
+        ):
+            arrays = self._mgr.arrays
+            if len(arrays) > 1 or (
+
+
+
+
+
+
+                not can_hold_element(arrays[0], fill_value)
+
+
+                and not (
+                    lib.is_integer(fill_value) and needs_i8_conversion(arrays[0].dtype)
+                )
+            ):
+
+
+                nper = abs(periods)
+                nper = min(nper, ncols)
+                if periods > 0:
+                    indexer = np.array(
+                        [-1] * nper + list(range(ncols - periods)), dtype=np.intp
+                    )
+                else:
+                    indexer = np.array(
+                        list(range(nper, ncols)) + [-1] * nper, dtype=np.intp
+                    )
+                mgr = self._mgr.reindex_indexer(
+                    self.columns,
+                    indexer,
+                    axis=0,
+                    fill_value=fill_value,
+                    allow_dups=True,
+                )
+                res_df = self._constructor(mgr)
+                return res_df.__finalize__(self, method="shift")
 
         return super().shift(
             periods=periods, freq=freq, axis=axis, fill_value=fill_value
```

```json
{
  "old_file": "R_candidates/Vi-1_v1.4.4/pandas.core.frame.DataFrame.shift.py",
  "new_file": "R_candidates/Vi_v1.5.0/pandas.core.frame.DataFrame.shift.py",
  "lines_added": 44,
  "lines_removed": 2
}
```
