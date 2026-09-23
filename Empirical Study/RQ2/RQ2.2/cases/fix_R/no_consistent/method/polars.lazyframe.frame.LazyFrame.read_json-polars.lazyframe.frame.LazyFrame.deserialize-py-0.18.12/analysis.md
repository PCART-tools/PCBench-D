# 一、突变情况分析

- **Total**: 121
- **替代API**: `polars.lazyframe.frame.LazyFrame.deserialize`
- **10% 阈值**: 12.1

## Vi-1 (py-0.18.12-py-0.20.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 1 | 0.9984 |
| tokenBased | 1 | 0.8289 |
| treeBased | 1 | 0.9706 |

## Vi (py-0.18.13-py-0.20.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 75 | 0.5505 |
| tokenBased | 1 | 0.3816 |
| treeBased | 13 | 0.5309 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 1 | 75 | -74 | true |
| tokenBased | 1 | 1 | +0 | false |
| treeBased | 1 | 13 | -12 | false |

```json
{
  "total": 121,
  "replacement_api": "polars.lazyframe.frame.LazyFrame.deserialize",
  "threshold_10pct": 12.1,
  "vi_minus_1": {
    "mapBased": {
      "rank": 1,
      "score": 0.998432
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.828947
    },
    "treeBased": {
      "rank": 1,
      "score": 0.970588
    }
  },
  "vi": {
    "mapBased": {
      "rank": 75,
      "score": 0.550505
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.381579
    },
    "treeBased": {
      "rank": 13,
      "score": 0.530864
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 1,
      "vi_rank": 75,
      "delta": -74,
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
      "vi_rank": 13,
      "delta": -12,
      "exceeds_10pct": false
    }
  ]
}
```

# 二、old → new Diff

- **old**: `polars.lazyframe.frame.LazyFrame.read_json/Vi-1_py-0.18.12.py`
- **new**: `polars.lazyframe.frame.LazyFrame.read_json/Vi_py-0.18.13.py`
- **+4 / -7**

```diff
--- polars.lazyframe.frame.LazyFrame.read_json/Vi-1_py-0.18.12.py
+++ polars.lazyframe.frame.LazyFrame.read_json/Vi_py-0.18.13.py
@@ -1,9 +1,6 @@
     @classmethod
-    def read_json(cls, file: str | Path | IOBase) -> Self:
+    @deprecate_renamed_function("deserialize", version="0.18.12")
+    @deprecate_renamed_parameter("file", "source", version="0.18.12")
+    def read_json(cls, source: str | Path | IOBase) -> Self:
         
-        if isinstance(file, StringIO):
-            file = BytesIO(file.getvalue().encode())
-        elif isinstance(file, (str, Path)):
-            file = normalise_filepath(file)
-
-        return cls._from_pyldf(PyLazyFrame.read_json(file))
+        return cls.deserialize(source)
```

```json
{
  "old_file": "polars.lazyframe.frame.LazyFrame.read_json/Vi-1_py-0.18.12.py",
  "new_file": "polars.lazyframe.frame.LazyFrame.read_json/Vi_py-0.18.13.py",
  "lines_added": 4,
  "lines_removed": 7
}
```
