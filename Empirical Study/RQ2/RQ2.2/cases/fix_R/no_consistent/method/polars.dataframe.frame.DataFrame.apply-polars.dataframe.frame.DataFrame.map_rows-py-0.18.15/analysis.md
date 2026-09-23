# 一、突变情况分析

- **Total**: 211
- **替代API**: `polars.dataframe.frame.DataFrame.map_rows`
- **10% 阈值**: 21.1

## Vi-1 (py-0.18.15-py-1.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 1 | 0.9985 |
| tokenBased | 1 | 0.8642 |
| treeBased | 1 | 0.9815 |

## Vi (py-0.19.0-py-1.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 127 | 0.5770 |
| tokenBased | 1 | 0.6420 |
| treeBased | 1 | 0.7158 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 1 | 127 | -126 | true |
| tokenBased | 1 | 1 | +0 | false |
| treeBased | 1 | 1 | +0 | false |

```json
{
  "total": 211,
  "replacement_api": "polars.dataframe.frame.DataFrame.map_rows",
  "threshold_10pct": 21.1,
  "vi_minus_1": {
    "mapBased": {
      "rank": 1,
      "score": 0.998512
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.864198
    },
    "treeBased": {
      "rank": 1,
      "score": 0.981481
    }
  },
  "vi": {
    "mapBased": {
      "rank": 127,
      "score": 0.577007
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.641975
    },
    "treeBased": {
      "rank": 1,
      "score": 0.715789
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 1,
      "vi_rank": 127,
      "delta": -126,
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
      "vi_rank": 1,
      "delta": 0,
      "exceeds_10pct": false
    }
  ]
}
```

# 二、old → new Diff

- **old**: `polars.dataframe.frame.DataFrame.apply/Vi-1_py-0.18.15.py`
- **new**: `polars.dataframe.frame.DataFrame.apply/Vi_py-0.19.0.py`
- **+2 / -9**

```diff
--- polars.dataframe.frame.DataFrame.apply/Vi-1_py-0.18.15.py
+++ polars.dataframe.frame.DataFrame.apply/Vi_py-0.19.0.py
@@ -1,3 +1,4 @@
+    @deprecate_renamed_function("map_rows", version="0.19.0")
     def apply(
         self,
         function: Callable[[tuple[Any, ...]], Any],
@@ -6,12 +7,4 @@
         inference_size: int = 256,
     ) -> DataFrame:
         
-
-
-
-
-        out, is_df = self._df.apply(function, return_dtype, inference_size)
-        if is_df:
-            return self._from_pydf(out)
-        else:
-            return wrap_s(out).to_frame()
+        return self.map_rows(function, return_dtype, inference_size=inference_size)
```

```json
{
  "old_file": "polars.dataframe.frame.DataFrame.apply/Vi-1_py-0.18.15.py",
  "new_file": "polars.dataframe.frame.DataFrame.apply/Vi_py-0.19.0.py",
  "lines_added": 2,
  "lines_removed": 9
}
```
