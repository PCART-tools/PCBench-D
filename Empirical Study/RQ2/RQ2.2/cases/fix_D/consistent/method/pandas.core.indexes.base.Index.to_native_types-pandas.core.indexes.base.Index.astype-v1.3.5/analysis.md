# 一、突变情况分析

- **Total**: 590
- **替代API**: `pandas.core.indexes.base.Index.astype`
- **10% 阈值**: 59.0

## Vi-1 (v1.1.5-v1.3.5)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 483 | 0.3543 |
| tokenBased | 290 | 0.2000 |
| treeBased | 467 | 0.3261 |

## Vi (v1.1.5-v1.4.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 507 | 0.3046 |
| tokenBased | 500 | 0.1228 |
| treeBased | 531 | 0.2388 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 483 | 507 | -24 | false |
| tokenBased | 290 | 500 | -210 | true |
| treeBased | 467 | 531 | -64 | true |

```json
{
  "total": 590,
  "replacement_api": "pandas.core.indexes.base.Index.astype",
  "threshold_10pct": 59.0,
  "vi_minus_1": {
    "mapBased": {
      "rank": 483,
      "score": 0.354308
    },
    "tokenBased": {
      "rank": 290,
      "score": 0.2
    },
    "treeBased": {
      "rank": 467,
      "score": 0.326087
    }
  },
  "vi": {
    "mapBased": {
      "rank": 507,
      "score": 0.30462
    },
    "tokenBased": {
      "rank": 500,
      "score": 0.122807
    },
    "treeBased": {
      "rank": 531,
      "score": 0.238806
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 483,
      "vi_rank": 507,
      "delta": -24,
      "exceeds_10pct": false
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 290,
      "vi_rank": 500,
      "delta": -210,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 467,
      "vi_rank": 531,
      "delta": -64,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `R_candidates/Vi-1_v1.3.5/pandas.core.indexes.base.Index.astype.py`
- **new**: `R_candidates/Vi_v1.4.0/pandas.core.indexes.base.Index.astype.py`
- **+30 / -10**

```diff
--- R_candidates/Vi-1_v1.3.5/pandas.core.indexes.base.Index.astype.py
+++ R_candidates/Vi_v1.4.0/pandas.core.indexes.base.Index.astype.py
@@ -1,20 +1,40 @@
-    def astype(self, dtype, copy=True):
+    def astype(self, dtype, copy: bool = True):
         
         if dtype is not None:
             dtype = pandas_dtype(dtype)
 
         if is_dtype_equal(self.dtype, dtype):
+
             return self.copy() if copy else self
+
+        if (
+            self.dtype == np.dtype("M8[ns]")
+            and isinstance(dtype, np.dtype)
+            and dtype.kind == "M"
+            and dtype != np.dtype("M8[ns]")
+        ):
+
+
+            raise TypeError(f"Cannot cast {type(self).__name__} to dtype")
+
+        values = self._data
+        if isinstance(values, ExtensionArray):
+            with rewrite_exception(type(values).__name__, type(self).__name__):
+                new_values = values.astype(dtype, copy=copy)
 
         elif isinstance(dtype, ExtensionDtype):
             cls = dtype.construct_array_type()
-            new_values = cls._from_sequence(self, dtype=dtype, copy=False)
-            return Index(new_values, dtype=dtype, copy=copy, name=self.name)
 
-        try:
-            casted = self._values.astype(dtype, copy=copy)
-        except (TypeError, ValueError) as err:
-            raise TypeError(
-                f"Cannot cast {type(self).__name__} to dtype {dtype}"
-            ) from err
-        return Index(casted, name=self.name, dtype=dtype)
+
+            new_values = cls._from_sequence(self, dtype=dtype, copy=copy)
+
+        else:
+            try:
+                new_values = values.astype(dtype, copy=copy)
+            except (TypeError, ValueError) as err:
+                raise TypeError(
+                    f"Cannot cast {type(self).__name__} to dtype {dtype}"
+                ) from err
+
+
+        return Index(new_values, name=self.name, dtype=new_values.dtype, copy=False)
```

```json
{
  "old_file": "R_candidates/Vi-1_v1.3.5/pandas.core.indexes.base.Index.astype.py",
  "new_file": "R_candidates/Vi_v1.4.0/pandas.core.indexes.base.Index.astype.py",
  "lines_added": 30,
  "lines_removed": 10
}
```
