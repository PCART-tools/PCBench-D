# 一、突变情况分析

- **Total**: 457
- **替代API**: `polars.expr.expr.Expr.map_elements`
- **10% 阈值**: 45.7

## Vi-1 (py-0.18.15-py-1.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 1 | 0.7850 |
| tokenBased | 1 | 0.7771 |
| treeBased | 1 | 0.8413 |

## Vi (py-0.19.0-py-1.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 425 | 0.4279 |
| tokenBased | 52 | 0.1941 |
| treeBased | 457 | 0.2134 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 1 | 425 | -424 | true |
| tokenBased | 1 | 52 | -51 | true |
| treeBased | 1 | 457 | -456 | true |

```json
{
  "total": 457,
  "replacement_api": "polars.expr.expr.Expr.map_elements",
  "threshold_10pct": 45.7,
  "vi_minus_1": {
    "mapBased": {
      "rank": 1,
      "score": 0.784987
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.777143
    },
    "treeBased": {
      "rank": 1,
      "score": 0.841317
    }
  },
  "vi": {
    "mapBased": {
      "rank": 425,
      "score": 0.427873
    },
    "tokenBased": {
      "rank": 52,
      "score": 0.194118
    },
    "treeBased": {
      "rank": 457,
      "score": 0.2134
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 1,
      "vi_rank": 425,
      "delta": -424,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 1,
      "vi_rank": 52,
      "delta": -51,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 1,
      "vi_rank": 457,
      "delta": -456,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `polars.expr.expr.Expr.apply/Vi-1_py-0.18.15.py`
- **new**: `polars.expr.expr.Expr.apply/Vi_py-0.19.0.py`
- **+9 / -68**

```diff
--- polars.expr.expr.Expr.apply/Vi-1_py-0.18.15.py
+++ polars.expr.expr.Expr.apply/Vi_py-0.19.0.py
@@ -1,3 +1,4 @@
+    @deprecate_renamed_function("map_elements", version="0.19.0")
     def apply(
         self,
         function: Callable[[Series], Series] | Callable[[Any], Any],
@@ -5,73 +6,13 @@
         *,
         skip_nulls: bool = True,
         pass_name: bool = False,
-        strategy: ApplyStrategy = "thread_local",
+        strategy: MapElementsStrategy = "thread_local",
     ) -> Self:
         
-
-        from polars.utils.udfs import warn_on_inefficient_apply
-
-        root_names = self.meta.root_names()
-        if len(root_names) > 0:
-            warn_on_inefficient_apply(function, columns=root_names, apply_target="expr")
-
-        if pass_name:
-
-            def wrap_f(x: Series) -> Series:
-                def inner(s: Series) -> Series:
-                    return function(s.alias(x.name))
-
-                with warnings.catch_warnings():
-                    warnings.simplefilter("ignore", PolarsInefficientApplyWarning)
-                    return x.apply(
-                        inner, return_dtype=return_dtype, skip_nulls=skip_nulls
-                    )
-
-        else:
-
-            def wrap_f(x: Series) -> Series:
-                with warnings.catch_warnings():
-                    warnings.simplefilter("ignore", PolarsInefficientApplyWarning)
-                    return x.apply(
-                        function, return_dtype=return_dtype, skip_nulls=skip_nulls
-                    )
-
-        if strategy == "thread_local":
-            return self.map(wrap_f, agg_list=True, return_dtype=return_dtype)
-        elif strategy == "threading":
-
-            def wrap_threading(x: Series) -> Series:
-                df = x.to_frame("x")
-
-                n_threads = threadpool_size()
-                chunk_size = x.len() // n_threads
-                remainder = x.len() % n_threads
-                if chunk_size == 0:
-                    chunk_sizes = [1 for _ in range(remainder)]
-                else:
-                    chunk_sizes = [
-                        chunk_size + 1 if i < remainder else chunk_size
-                        for i in range(n_threads)
-                    ]
-
-                def get_lazy_promise(df: DataFrame) -> LazyFrame:
-                    return df.lazy().select(
-                        F.col("x").map(wrap_f, agg_list=True, return_dtype=return_dtype)
-                    )
-
-
-
-                partitions = []
-                b = 0
-                for step in chunk_sizes:
-                    a = b
-                    b = b + step
-                    partition_df = df[a:b]
-                    partitions.append(get_lazy_promise(partition_df))
-
-                out = [df.to_series() for df in F.collect_all(partitions)]
-                return F.concat(out, rechunk=False)
-
-            return self.map(wrap_threading, agg_list=True, return_dtype=return_dtype)
-        else:
-            ValueError(f"Strategy {strategy} is not supported.")
+        return self.map_elements(
+            function,
+            return_dtype=return_dtype,
+            skip_nulls=skip_nulls,
+            pass_name=pass_name,
+            strategy=strategy,
+        )
```

```json
{
  "old_file": "polars.expr.expr.Expr.apply/Vi-1_py-0.18.15.py",
  "new_file": "polars.expr.expr.Expr.apply/Vi_py-0.19.0.py",
  "lines_added": 9,
  "lines_removed": 68
}
```
