# 一、突变情况分析

- **Total**: 417
- **替代API**: `pandas.io.formats.style.Styler.to_html`
- **10% 阈值**: 41.7

## Vi-1 (v1.3.5-v2.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 245 | 0.3798 |
| tokenBased | 133 | 0.2298 |
| treeBased | 244 | 0.3468 |

## Vi (v1.4.0-v2.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 212 | 0.3885 |
| tokenBased | 107 | 0.2574 |
| treeBased | 198 | 0.3658 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 245 | 212 | +33 | false |
| tokenBased | 133 | 107 | +26 | false |
| treeBased | 244 | 198 | +46 | true |

```json
{
  "total": 417,
  "replacement_api": "pandas.io.formats.style.Styler.to_html",
  "threshold_10pct": 41.7,
  "vi_minus_1": {
    "mapBased": {
      "rank": 245,
      "score": 0.379768
    },
    "tokenBased": {
      "rank": 133,
      "score": 0.229787
    },
    "treeBased": {
      "rank": 244,
      "score": 0.346774
    }
  },
  "vi": {
    "mapBased": {
      "rank": 212,
      "score": 0.388458
    },
    "tokenBased": {
      "rank": 107,
      "score": 0.257384
    },
    "treeBased": {
      "rank": 198,
      "score": 0.365759
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 245,
      "vi_rank": 212,
      "delta": 33,
      "exceeds_10pct": false
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 133,
      "vi_rank": 107,
      "delta": 26,
      "exceeds_10pct": false
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 244,
      "vi_rank": 198,
      "delta": 46,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `pandas.io.formats.style.Styler.render/Vi-1_v1.3.5.py`
- **new**: `pandas.io.formats.style.Styler.render/Vi_v1.4.0.py`
- **+5 / -0**

```diff
--- pandas.io.formats.style.Styler.render/Vi-1_v1.3.5.py
+++ pandas.io.formats.style.Styler.render/Vi_v1.4.0.py
@@ -5,6 +5,11 @@
         **kwargs,
     ) -> str:
         
+        warnings.warn(
+            "this method is deprecated in favour of `Styler.to_html()`",
+            FutureWarning,
+            stacklevel=find_stack_level(),
+        )
         if sparse_index is None:
             sparse_index = get_option("styler.sparse.index")
         if sparse_columns is None:
```

```json
{
  "old_file": "pandas.io.formats.style.Styler.render/Vi-1_v1.3.5.py",
  "new_file": "pandas.io.formats.style.Styler.render/Vi_v1.4.0.py",
  "lines_added": 5,
  "lines_removed": 0
}
```
