# 一、突变情况分析

- **Total**: 21
- **替代API**: `pandas.core.indexes.base.Index`
- **10% 阈值**: 2.1

## Vi-1 (v1.4.4-v2.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 8 | 0.0093 |
| tokenBased | 21 | 0.0031 |

## Vi (v1.5.0-v2.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 19 | 0.0122 |
| tokenBased | 21 | 0.0040 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 8 | 19 | -11 | true |
| tokenBased | 21 | 21 | +0 | false |

```json
{
  "total": 21,
  "replacement_api": "pandas.core.indexes.base.Index",
  "threshold_10pct": 2.1,
  "vi_minus_1": {
    "mapBased": {
      "rank": 8,
      "score": 0.009259
    },
    "tokenBased": {
      "rank": 21,
      "score": 0.00306
    }
  },
  "vi": {
    "mapBased": {
      "rank": 19,
      "score": 0.012249
    },
    "tokenBased": {
      "rank": 21,
      "score": 0.003952
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 8,
      "vi_rank": 19,
      "delta": -11,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 21,
      "vi_rank": 21,
      "delta": 0,
      "exceeds_10pct": false
    }
  ]
}
```

# 二、old → new Diff

- **old**: `pandas.core.indexes.numeric.Float64Index/Vi-1_v1.4.4.py`
- **new**: `pandas.core.indexes.numeric.Float64Index/Vi_v1.5.0.py`
- **+4 / -1**

```diff
--- pandas.core.indexes.numeric.Float64Index/Vi-1_v1.4.4.py
+++ pandas.core.indexes.numeric.Float64Index/Vi_v1.5.0.py
@@ -8,7 +8,10 @@
     __doc__ = _num_index_shared_docs["class_descr"] % _index_descr_args
 
     _typ = "float64index"
-    _engine_type = libindex.Float64Engine
     _default_dtype = np.dtype(np.float64)
     _dtype_validation_metadata = (is_float_dtype, "float")
     _is_backward_compat_public_numeric_index: bool = False
+
+    @property
+    def _engine_type(self) -> type[libindex.Float64Engine]:
+        return libindex.Float64Engine
```

```json
{
  "old_file": "pandas.core.indexes.numeric.Float64Index/Vi-1_v1.4.4.py",
  "new_file": "pandas.core.indexes.numeric.Float64Index/Vi_v1.5.0.py",
  "lines_added": 4,
  "lines_removed": 1
}
```
