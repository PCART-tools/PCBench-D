# 一、突变情况分析

- **Total**: 417
- **替代API**: `pandas.io.formats.style.Styler.hide`
- **10% 阈值**: 41.7

## Vi-1 (v1.3.5-v2.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 292 | 0.3195 |
| tokenBased | 86 | 0.2683 |
| treeBased | 198 | 0.3764 |

## Vi (v1.4.0-v2.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 373 | 0.2511 |
| tokenBased | 28 | 0.2573 |
| treeBased | 324 | 0.2992 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 292 | 373 | -81 | true |
| tokenBased | 86 | 28 | +58 | true |
| treeBased | 198 | 324 | -126 | true |

```json
{
  "total": 417,
  "replacement_api": "pandas.io.formats.style.Styler.hide",
  "threshold_10pct": 41.7,
  "vi_minus_1": {
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
  "vi": {
    "mapBased": {
      "rank": 373,
      "score": 0.251118
    },
    "tokenBased": {
      "rank": 28,
      "score": 0.257282
    },
    "treeBased": {
      "rank": 324,
      "score": 0.299213
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 292,
      "vi_rank": 373,
      "delta": -81,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 86,
      "vi_rank": 28,
      "delta": 58,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 198,
      "vi_rank": 324,
      "delta": -126,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `pandas.io.formats.style.Styler.hide_index/Vi-1_v1.3.5.py`
- **new**: `pandas.io.formats.style.Styler.hide_index/Vi_v1.4.0.py`
- **+12 / -12**

```diff
--- pandas.io.formats.style.Styler.hide_index/Vi-1_v1.3.5.py
+++ pandas.io.formats.style.Styler.hide_index/Vi_v1.4.0.py
@@ -1,13 +1,13 @@
-    def hide_index(self, subset: Subset | None = None) -> Styler:
+    def hide_index(
+        self,
+        subset: Subset | None = None,
+        level: Level | list[Level] | None = None,
+        names: bool = False,
+    ) -> Styler:
         
-        if subset is None:
-            self.hide_index_ = True
-        else:
-            subset_ = IndexSlice[subset, :]
-            subset = non_reducing_slice(subset_)
-            hide = self.data.loc[subset]
-            hrows = self.index.get_indexer_for(hide.index)
-
-
-            self.hidden_rows = hrows
-        return self
+        warnings.warn(
+            "this method is deprecated in favour of `Styler.hide(axis='index')`",
+            FutureWarning,
+            stacklevel=find_stack_level(),
+        )
+        return self.hide(axis=0, level=level, subset=subset, names=names)
```

```json
{
  "old_file": "pandas.io.formats.style.Styler.hide_index/Vi-1_v1.3.5.py",
  "new_file": "pandas.io.formats.style.Styler.hide_index/Vi_v1.4.0.py",
  "lines_added": 12,
  "lines_removed": 12
}
```
