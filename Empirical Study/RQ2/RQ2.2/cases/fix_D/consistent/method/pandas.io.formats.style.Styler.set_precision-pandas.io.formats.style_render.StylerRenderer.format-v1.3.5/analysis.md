# 一、突变情况分析

- **Total**: 384
- **替代API**: `pandas.io.formats.style_render.StylerRenderer.format`
- **10% 阈值**: 38.4

## Vi-1 (v1.2.5-v1.3.5)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 347 | 0.2183 |
| tokenBased | 323 | 0.0788 |
| treeBased | 355 | 0.1276 |

## Vi (v1.2.5-v1.4.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 379 | 0.2112 |
| tokenBased | 363 | 0.0737 |
| treeBased | 384 | 0.1202 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 347 | 379 | -32 | false |
| tokenBased | 323 | 363 | -40 | true |
| treeBased | 355 | 384 | -29 | false |

```json
{
  "total": 384,
  "replacement_api": "pandas.io.formats.style_render.StylerRenderer.format",
  "threshold_10pct": 38.4,
  "vi_minus_1": {
    "mapBased": {
      "rank": 347,
      "score": 0.218332
    },
    "tokenBased": {
      "rank": 323,
      "score": 0.078818
    },
    "treeBased": {
      "rank": 355,
      "score": 0.127551
    }
  },
  "vi": {
    "mapBased": {
      "rank": 379,
      "score": 0.211155
    },
    "tokenBased": {
      "rank": 363,
      "score": 0.073733
    },
    "treeBased": {
      "rank": 384,
      "score": 0.120192
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 347,
      "vi_rank": 379,
      "delta": -32,
      "exceeds_10pct": false
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 323,
      "vi_rank": 363,
      "delta": -40,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 355,
      "vi_rank": 384,
      "delta": -29,
      "exceeds_10pct": false
    }
  ]
}
```

# 二、old → new Diff

- **old**: `R_candidates/Vi-1_v1.3.5/pandas.io.formats.style_render.StylerRenderer.format.py`
- **new**: `R_candidates/Vi_v1.4.0/pandas.io.formats.style_render.StylerRenderer.format.py`
- **+3 / -0**

```diff
--- R_candidates/Vi-1_v1.3.5/pandas.io.formats.style_render.StylerRenderer.format.py
+++ R_candidates/Vi_v1.4.0/pandas.io.formats.style_render.StylerRenderer.format.py
@@ -7,6 +7,7 @@
         decimal: str = ".",
         thousands: str | None = None,
         escape: str | None = None,
+        hyperlinks: str | None = None,
     ) -> StylerRenderer:
         
         if all(
@@ -18,6 +19,7 @@
                 thousands is None,
                 na_rep is None,
                 escape is None,
+                hyperlinks is None,
             )
         ):
             self._display_funcs.clear()
@@ -40,6 +42,7 @@
                 decimal=decimal,
                 thousands=thousands,
                 escape=escape,
+                hyperlinks=hyperlinks,
             )
             for ri in ris:
                 self._display_funcs[(ri, ci)] = format_func
```

```json
{
  "old_file": "R_candidates/Vi-1_v1.3.5/pandas.io.formats.style_render.StylerRenderer.format.py",
  "new_file": "R_candidates/Vi_v1.4.0/pandas.io.formats.style_render.StylerRenderer.format.py",
  "lines_added": 3,
  "lines_removed": 0
}
```
