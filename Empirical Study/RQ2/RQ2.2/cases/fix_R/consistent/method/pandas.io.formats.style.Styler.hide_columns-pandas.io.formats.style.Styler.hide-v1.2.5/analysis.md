# 一、突变情况分析

- **Total**: 417
- **替代API**: `pandas.io.formats.style.Styler.hide`
- **10% 阈值**: 41.7

## Vi-1 (v1.2.5-v2.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 382 | 0.2823 |
| tokenBased | 302 | 0.1520 |
| treeBased | 377 | 0.2194 |

## Vi (v1.3.0-v2.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 292 | 0.3195 |
| tokenBased | 84 | 0.2683 |
| treeBased | 198 | 0.3764 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 382 | 292 | +90 | true |
| tokenBased | 302 | 84 | +218 | true |
| treeBased | 377 | 198 | +179 | true |

```json
{
  "total": 417,
  "replacement_api": "pandas.io.formats.style.Styler.hide",
  "threshold_10pct": 41.7,
  "vi_minus_1": {
    "mapBased": {
      "rank": 382,
      "score": 0.282329
    },
    "tokenBased": {
      "rank": 302,
      "score": 0.151961
    },
    "treeBased": {
      "rank": 377,
      "score": 0.219409
    }
  },
  "vi": {
    "mapBased": {
      "rank": 292,
      "score": 0.31952
    },
    "tokenBased": {
      "rank": 84,
      "score": 0.268293
    },
    "treeBased": {
      "rank": 198,
      "score": 0.376426
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 382,
      "vi_rank": 292,
      "delta": 90,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 302,
      "vi_rank": 84,
      "delta": 218,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 377,
      "vi_rank": 198,
      "delta": 179,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `pandas.io.formats.style.Styler.hide_columns/Vi-1_v1.2.5.py`
- **new**: `pandas.io.formats.style.Styler.hide_columns/Vi_v1.3.0.py`
- **+11 / -4**

```diff
--- pandas.io.formats.style.Styler.hide_columns/Vi-1_v1.2.5.py
+++ pandas.io.formats.style.Styler.hide_columns/Vi_v1.3.0.py
@@ -1,6 +1,13 @@
-    def hide_columns(self, subset) -> "Styler":
+    def hide_columns(self, subset: Subset | None = None) -> Styler:
         
-        subset = non_reducing_slice(subset)
-        hidden_df = self.data.loc[subset]
-        self.hidden_columns = self.columns.get_indexer_for(hidden_df.columns)
+        if subset is None:
+            self.hide_columns_ = True
+        else:
+            subset_ = IndexSlice[:, subset]
+            subset = non_reducing_slice(subset_)
+            hide = self.data.loc[subset]
+            hcols = self.columns.get_indexer_for(hide.columns)
+
+
+            self.hidden_columns = hcols
         return self
```

```json
{
  "old_file": "pandas.io.formats.style.Styler.hide_columns/Vi-1_v1.2.5.py",
  "new_file": "pandas.io.formats.style.Styler.hide_columns/Vi_v1.3.0.py",
  "lines_added": 11,
  "lines_removed": 4
}
```
