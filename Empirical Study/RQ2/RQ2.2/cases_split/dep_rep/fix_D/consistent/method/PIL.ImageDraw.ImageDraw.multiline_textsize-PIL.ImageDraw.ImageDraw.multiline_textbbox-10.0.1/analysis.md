# 一、突变情况分析

- **Total**: 800
- **替代API**: `PIL.ImageDraw.ImageDraw.multiline_textbbox`
- **10% 阈值**: 80.0

## Vi-1 (9.5.0-10.0.1)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 89 | 0.3672 |
| tokenBased | 272 | 0.2530 |
| treeBased | 391 | 0.3142 |

## Vi (9.5.0-10.1.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 272 | 0.2916 |
| tokenBased | 294 | 0.2441 |
| treeBased | 410 | 0.3041 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 89 | 272 | -183 | true |
| tokenBased | 272 | 294 | -22 | false |
| treeBased | 391 | 410 | -19 | false |

```json
{
  "total": 800,
  "replacement_api": "PIL.ImageDraw.ImageDraw.multiline_textbbox",
  "threshold_10pct": 80.0,
  "vi_minus_1": {
    "mapBased": {
      "rank": 89,
      "score": 0.367155
    },
    "tokenBased": {
      "rank": 272,
      "score": 0.253049
    },
    "treeBased": {
      "rank": 391,
      "score": 0.314159
    }
  },
  "vi": {
    "mapBased": {
      "rank": 272,
      "score": 0.291634
    },
    "tokenBased": {
      "rank": 294,
      "score": 0.244118
    },
    "treeBased": {
      "rank": 410,
      "score": 0.304069
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 89,
      "vi_rank": 272,
      "delta": -183,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 272,
      "vi_rank": 294,
      "delta": -22,
      "exceeds_10pct": false
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 391,
      "vi_rank": 410,
      "delta": -19,
      "exceeds_10pct": false
    }
  ]
}
```

# 二、old → new Diff

- **old**: `R_candidates/Vi-1_10.0.1/PIL.ImageDraw.ImageDraw.multiline_textbbox.py`
- **new**: `R_candidates/Vi_10.1.0/PIL.ImageDraw.ImageDraw.multiline_textbbox.py`
- **+5 / -0**

```diff
--- R_candidates/Vi-1_10.0.1/PIL.ImageDraw.ImageDraw.multiline_textbbox.py
+++ R_candidates/Vi_10.1.0/PIL.ImageDraw.ImageDraw.multiline_textbbox.py
@@ -11,6 +11,8 @@
         language=None,
         stroke_width=0,
         embedded_color=False,
+        *,
+        font_size=None,
     ):
         if direction == "ttb":
             msg = "ttb direction is unsupported for multiline text"
@@ -24,6 +26,9 @@
         elif anchor[1] in "tb":
             msg = "anchor not supported for multiline text"
             raise ValueError(msg)
+
+        if font is None:
+            font = self._getfont(font_size)
 
         widths = []
         max_width = 0
```

```json
{
  "old_file": "R_candidates/Vi-1_10.0.1/PIL.ImageDraw.ImageDraw.multiline_textbbox.py",
  "new_file": "R_candidates/Vi_10.1.0/PIL.ImageDraw.ImageDraw.multiline_textbbox.py",
  "lines_added": 5,
  "lines_removed": 0
}
```
