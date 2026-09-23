# 一、突变情况分析

- **Total**: 3392
- **替代API**: `pandas.core.frame.DataFrame.shift`
- **10% 阈值**: 339.2

## Vi-1 (v1.1.5-v2.0.3)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 1334 | 0.3247 |
| tokenBased | 1219 | 0.2266 |
| treeBased | 1892 | 0.3155 |

## Vi (v1.1.5-v2.1.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 2930 | 0.2004 |
| tokenBased | 1901 | 0.1631 |
| treeBased | 2542 | 0.2375 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 1334 | 2930 | -1596 | true |
| tokenBased | 1219 | 1901 | -682 | true |
| treeBased | 1892 | 2542 | -650 | true |

```json
{
  "total": 3392,
  "replacement_api": "pandas.core.frame.DataFrame.shift",
  "threshold_10pct": 339.2,
  "vi_minus_1": {
    "mapBased": {
      "rank": 1334,
      "score": 0.324734
    },
    "tokenBased": {
      "rank": 1219,
      "score": 0.226586
    },
    "treeBased": {
      "rank": 1892,
      "score": 0.315534
    }
  },
  "vi": {
    "mapBased": {
      "rank": 2930,
      "score": 0.20036
    },
    "tokenBased": {
      "rank": 1901,
      "score": 0.163136
    },
    "treeBased": {
      "rank": 2542,
      "score": 0.2375
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 1334,
      "vi_rank": 2930,
      "delta": -1596,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 1219,
      "vi_rank": 1901,
      "delta": -682,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 1892,
      "vi_rank": 2542,
      "delta": -650,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `R_candidates/Vi-1_v2.0.3/pandas.core.frame.DataFrame.shift.py`
- **new**: `R_candidates/Vi_v2.1.0/pandas.core.frame.DataFrame.shift.py`
- **+62 / -32**

```diff
--- R_candidates/Vi-1_v2.0.3/pandas.core.frame.DataFrame.shift.py
+++ R_candidates/Vi_v2.1.0/pandas.core.frame.DataFrame.shift.py
@@ -1,52 +1,80 @@
     @doc(NDFrame.shift, klass=_shared_doc_kwargs["klass"])
     def shift(
         self,
-        periods: int = 1,
+        periods: int | Sequence[int] = 1,
         freq: Frequency | None = None,
         axis: Axis = 0,
         fill_value: Hashable = lib.no_default,
+        suffix: str | None = None,
     ) -> DataFrame:
+        if freq is not None and fill_value is not lib.no_default:
+
+            warnings.warn(
+                "Passing a 'freq' together with a 'fill_value' silently ignores "
+                "the fill_value and is deprecated. This will raise in a future "
+                "version.",
+                FutureWarning,
+                stacklevel=find_stack_level(),
+            )
+            fill_value = lib.no_default
+
         axis = self._get_axis_number(axis)
 
+        if is_list_like(periods):
+            periods = cast(Sequence, periods)
+            if axis == 1:
+                raise ValueError(
+                    "If `periods` contains multiple shifts, `axis` cannot be 1."
+                )
+            if len(periods) == 0:
+                raise ValueError("If `periods` is an iterable, it cannot be empty.")
+            from pandas.core.reshape.concat import concat
+
+            shifted_dataframes = []
+            for period in periods:
+                if not is_integer(period):
+                    raise TypeError(
+                        f"Periods must be integer, but {period} is {type(period)}."
+                    )
+                period = cast(int, period)
+                shifted_dataframes.append(
+                    super()
+                    .shift(periods=period, freq=freq, axis=axis, fill_value=fill_value)
+                    .add_suffix(f"{suffix}_{period}" if suffix else f"_{period}")
+                )
+            return concat(shifted_dataframes, axis=1)
+        elif suffix:
+            raise ValueError("Cannot specify `suffix` if `periods` is an int.")
+        periods = cast(int, periods)
+
         ncols = len(self.columns)
-        if (
-            axis == 1
-            and periods != 0
-            and freq is None
-            and fill_value is lib.no_default
-            and ncols > 0
-        ):
+        arrays = self._mgr.arrays
+        if axis == 1 and periods != 0 and ncols > 0 and freq is None:
+            if fill_value is lib.no_default:
 
 
 
-            label = self.columns[0]
+                label = self.columns[0]
 
-            if periods > 0:
-                result = self.iloc[:, :-periods]
-                for col in range(min(ncols, abs(periods))):
+                if periods > 0:
+                    result = self.iloc[:, :-periods]
+                    for col in range(min(ncols, abs(periods))):
 
 
-                    filler = self.iloc[:, 0].shift(len(self))
-                    result.insert(0, label, filler, allow_duplicates=True)
-            else:
-                result = self.iloc[:, -periods:]
-                for col in range(min(ncols, abs(periods))):
+                        filler = self.iloc[:, 0].shift(len(self))
+                        result.insert(0, label, filler, allow_duplicates=True)
+                else:
+                    result = self.iloc[:, -periods:]
+                    for col in range(min(ncols, abs(periods))):
 
-                    filler = self.iloc[:, -1].shift(len(self))
-                    result.insert(
-                        len(result.columns), label, filler, allow_duplicates=True
-                    )
+                        filler = self.iloc[:, -1].shift(len(self))
+                        result.insert(
+                            len(result.columns), label, filler, allow_duplicates=True
+                        )
 
-            result.columns = self.columns.copy()
-            return result
-        elif (
-            axis == 1
-            and periods != 0
-            and fill_value is not lib.no_default
-            and ncols > 0
-        ):
-            arrays = self._mgr.arrays
-            if len(arrays) > 1 or (
+                result.columns = self.columns.copy()
+                return result
+            elif len(arrays) > 1 or (
 
 
 
@@ -72,8 +100,10 @@
                     fill_value=fill_value,
                     allow_dups=True,
                 )
-                res_df = self._constructor(mgr)
+                res_df = self._constructor_from_mgr(mgr, axes=mgr.axes)
                 return res_df.__finalize__(self, method="shift")
+            else:
+                return self.T.shift(periods=periods, fill_value=fill_value).T
 
         return super().shift(
             periods=periods, freq=freq, axis=axis, fill_value=fill_value
```

```json
{
  "old_file": "R_candidates/Vi-1_v2.0.3/pandas.core.frame.DataFrame.shift.py",
  "new_file": "R_candidates/Vi_v2.1.0/pandas.core.frame.DataFrame.shift.py",
  "lines_added": 62,
  "lines_removed": 32
}
```
