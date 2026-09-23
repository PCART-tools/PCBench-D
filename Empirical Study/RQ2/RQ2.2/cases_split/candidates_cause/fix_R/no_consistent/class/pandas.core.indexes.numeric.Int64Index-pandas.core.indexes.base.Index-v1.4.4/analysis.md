# 一、突变情况分析

- **Total**: 21
- **替代API**: `pandas.core.indexes.base.Index`
- **10% 阈值**: 2.1

## Vi-1 (v1.4.4-v2.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 8 | 0.0096 |
| tokenBased | 21 | 0.0029 |

## Vi (v1.5.0-v2.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 19 | 0.0126 |
| tokenBased | 21 | 0.0038 |

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
      "score": 0.009615
    },
    "tokenBased": {
      "rank": 21,
      "score": 0.002869
    }
  },
  "vi": {
    "mapBased": {
      "rank": 19,
      "score": 0.012633
    },
    "tokenBased": {
      "rank": 21,
      "score": 0.003761
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

- **old**: `pandas.core.indexes.numeric.Int64Index/Vi-1_v1.4.4.py`
- **new**: `pandas.core.indexes.numeric.Int64Index/Vi_v1.5.0.py`
- **+4 / -1**

```diff
--- pandas.core.indexes.numeric.Int64Index/Vi-1_v1.4.4.py
+++ pandas.core.indexes.numeric.Int64Index/Vi_v1.5.0.py
@@ -8,6 +8,9 @@
     __doc__ = _num_index_shared_docs["class_descr"] % _index_descr_args
 
     _typ = "int64index"
-    _engine_type = libindex.Int64Engine
     _default_dtype = np.dtype(np.int64)
     _dtype_validation_metadata = (is_signed_integer_dtype, "signed integer")
+
+    @property
+    def _engine_type(self) -> type[libindex.Int64Engine]:
+        return libindex.Int64Engine
```

```json
{
  "old_file": "pandas.core.indexes.numeric.Int64Index/Vi-1_v1.4.4.py",
  "new_file": "pandas.core.indexes.numeric.Int64Index/Vi_v1.5.0.py",
  "lines_added": 4,
  "lines_removed": 1
}
```
