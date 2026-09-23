# 一、突变情况分析

- **Total**: 176
- **替代API**: `polars.internals.dataframe.frame.DataFrame.iter_rows`
- **10% 阈值**: 17.6

## Vi-1 (py-0.15.17-py-0.16.1)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 152 | 0.2319 |
| tokenBased | 36 | 0.1151 |
| treeBased | 149 | 0.2500 |

## Vi (py-0.15.17-py-0.16.2)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 156 | 0.2220 |
| tokenBased | 55 | 0.1026 |
| treeBased | 156 | 0.2240 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 152 | 156 | -4 | false |
| tokenBased | 36 | 55 | -19 | true |
| treeBased | 149 | 156 | -7 | false |

```json
{
  "total": 176,
  "replacement_api": "polars.internals.dataframe.frame.DataFrame.iter_rows",
  "threshold_10pct": 17.6,
  "vi_minus_1": {
    "mapBased": {
      "rank": 152,
      "score": 0.231855
    },
    "tokenBased": {
      "rank": 36,
      "score": 0.115108
    },
    "treeBased": {
      "rank": 149,
      "score": 0.25
    }
  },
  "vi": {
    "mapBased": {
      "rank": 156,
      "score": 0.222008
    },
    "tokenBased": {
      "rank": 55,
      "score": 0.102564
    },
    "treeBased": {
      "rank": 156,
      "score": 0.224044
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 152,
      "vi_rank": 156,
      "delta": -4,
      "exceeds_10pct": false
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 36,
      "vi_rank": 55,
      "delta": -19,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 149,
      "vi_rank": 156,
      "delta": -7,
      "exceeds_10pct": false
    }
  ]
}
```

# 二、old → new Diff

- **old**: `R_candidates/Vi-1_py-0.16.1/polars.internals.dataframe.frame.DataFrame.iter_rows.py`
- **new**: `R_candidates/Vi_py-0.16.2/polars.internals.dataframe.frame.DataFrame.iter_rows.py`
- **+7 / -1**

```diff
--- R_candidates/Vi-1_py-0.16.1/polars.internals.dataframe.frame.DataFrame.iter_rows.py
+++ R_candidates/Vi_py-0.16.2/polars.internals.dataframe.frame.DataFrame.iter_rows.py
@@ -8,9 +8,15 @@
 
 
         if buffer_size:
+            load_pyarrow_dicts = (
+                named
+                and _PYARROW_AVAILABLE
+
+                and not any((getattr(tp, "tu", None) == "ns") for tp in self.dtypes)
+            )
             for offset in range(0, self.height, buffer_size):
                 zerocopy_slice = self.slice(offset, buffer_size)
-                if named and _PYARROW_AVAILABLE:
+                if load_pyarrow_dicts:
                     yield from zerocopy_slice.to_arrow().to_batches()[0].to_pylist()
                 else:
                     rows_chunk = zerocopy_slice.rows(named=False)
```

```json
{
  "old_file": "R_candidates/Vi-1_py-0.16.1/polars.internals.dataframe.frame.DataFrame.iter_rows.py",
  "new_file": "R_candidates/Vi_py-0.16.2/polars.internals.dataframe.frame.DataFrame.iter_rows.py",
  "lines_added": 7,
  "lines_removed": 1
}
```
