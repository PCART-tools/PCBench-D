# 一、突变情况分析

- **Total**: 430
- **替代API**: `polars.series.string.StringNameSpace.json_decode`
- **10% 阈值**: 43.0

## Vi-1 (py-0.19.14-py-1.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 1 | 1.0000 |
| tokenBased | 1 | 0.8182 |
| treeBased | 1 | 0.8947 |

## Vi (py-0.19.15-py-1.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 81 | 0.7652 |
| tokenBased | 1 | 0.7400 |
| treeBased | 2 | 0.6939 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 1 | 81 | -80 | true |
| tokenBased | 1 | 1 | +0 | false |
| treeBased | 1 | 2 | -1 | false |

```json
{
  "total": 430,
  "replacement_api": "polars.series.string.StringNameSpace.json_decode",
  "threshold_10pct": 43.0,
  "vi_minus_1": {
    "mapBased": {
      "rank": 1,
      "score": 1.0
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.818182
    },
    "treeBased": {
      "rank": 1,
      "score": 0.894737
    }
  },
  "vi": {
    "mapBased": {
      "rank": 81,
      "score": 0.765217
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.74
    },
    "treeBased": {
      "rank": 2,
      "score": 0.693878
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 1,
      "vi_rank": 81,
      "delta": -80,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 1,
      "vi_rank": 1,
      "delta": 0,
      "exceeds_10pct": false
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 1,
      "vi_rank": 2,
      "delta": -1,
      "exceeds_10pct": false
    }
  ]
}
```

# 二、old → new Diff

- **old**: `polars.series.string.StringNameSpace.json_extract/Vi-1_py-0.19.14.py`
- **new**: `polars.series.string.StringNameSpace.json_extract/Vi_py-0.19.15.py`
- **+2 / -0**

```diff
--- polars.series.string.StringNameSpace.json_extract/Vi-1_py-0.19.14.py
+++ polars.series.string.StringNameSpace.json_extract/Vi_py-0.19.15.py
@@ -1,4 +1,6 @@
+    @deprecate_renamed_function("json_decode", version="0.19.15")
     def json_extract(
         self, dtype: PolarsDataType | None = None, infer_schema_length: int | None = 100
     ) -> Series:
         
+        return self.json_decode(dtype, infer_schema_length)
```

```json
{
  "old_file": "polars.series.string.StringNameSpace.json_extract/Vi-1_py-0.19.14.py",
  "new_file": "polars.series.string.StringNameSpace.json_extract/Vi_py-0.19.15.py",
  "lines_added": 2,
  "lines_removed": 0
}
```
