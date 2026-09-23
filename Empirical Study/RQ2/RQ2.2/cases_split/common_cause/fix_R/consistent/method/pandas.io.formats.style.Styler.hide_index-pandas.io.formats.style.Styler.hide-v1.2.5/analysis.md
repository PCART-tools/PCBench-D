# 一、突变情况分析

- **Total**: 417
- **替代API**: `pandas.io.formats.style.Styler.hide`
- **10% 阈值**: 41.7

## Vi-1 (v1.2.5-v2.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 377 | 0.1887 |
| tokenBased | 331 | 0.0690 |
| treeBased | 395 | 0.1005 |

## Vi (v1.3.0-v2.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 292 | 0.3195 |
| tokenBased | 86 | 0.2683 |
| treeBased | 198 | 0.3764 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 377 | 292 | +85 | true |
| tokenBased | 331 | 86 | +245 | true |
| treeBased | 395 | 198 | +197 | true |

```json
{
  "total": 417,
  "replacement_api": "pandas.io.formats.style.Styler.hide",
  "threshold_10pct": 41.7,
  "vi_minus_1": {
    "mapBased": {
      "rank": 377,
      "score": 0.188702
    },
    "tokenBased": {
      "rank": 331,
      "score": 0.068966
    },
    "treeBased": {
      "rank": 395,
      "score": 0.100457
    }
  },
  "vi": {
    "mapBased": {
      "rank": 292,
      "score": 0.31952
    },
    "tokenBased": {
      "rank": 86,
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
      "vi1_rank": 377,
      "vi_rank": 292,
      "delta": 85,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 331,
      "vi_rank": 86,
      "delta": 245,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 395,
      "vi_rank": 198,
      "delta": 197,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `pandas.io.formats.style.Styler.hide_index/Vi-1_v1.2.5.py`
- **new**: `pandas.io.formats.style.Styler.hide_index/Vi_v1.3.0.py`
- **+11 / -2**

```diff
--- pandas.io.formats.style.Styler.hide_index/Vi-1_v1.2.5.py
+++ pandas.io.formats.style.Styler.hide_index/Vi_v1.3.0.py
@@ -1,4 +1,13 @@
-    def hide_index(self) -> "Styler":
+    def hide_index(self, subset: Subset | None = None) -> Styler:
         
-        self.hidden_index = True
+        if subset is None:
+            self.hide_index_ = True
+        else:
+            subset_ = IndexSlice[subset, :]
+            subset = non_reducing_slice(subset_)
+            hide = self.data.loc[subset]
+            hrows = self.index.get_indexer_for(hide.index)
+
+
+            self.hidden_rows = hrows
         return self
```

```json
{
  "old_file": "pandas.io.formats.style.Styler.hide_index/Vi-1_v1.2.5.py",
  "new_file": "pandas.io.formats.style.Styler.hide_index/Vi_v1.3.0.py",
  "lines_added": 11,
  "lines_removed": 2
}
```
