# 一、突变情况分析

- **Total**: 800
- **替代API**: `PIL.ImageDraw.ImageDraw.multiline_textbbox`
- **10% 阈值**: 80.0

## Vi-1 (9.5.0-10.0.1)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 320 | 0.3001 |
| tokenBased | 311 | 0.2424 |
| treeBased | 441 | 0.2927 |

## Vi (9.5.0-10.1.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 575 | 0.2372 |
| tokenBased | 324 | 0.2339 |
| treeBased | 476 | 0.2811 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 320 | 575 | -255 | true |
| tokenBased | 311 | 324 | -13 | false |
| treeBased | 441 | 476 | -35 | false |

```json
{
  "total": 800,
  "replacement_api": "PIL.ImageDraw.ImageDraw.multiline_textbbox",
  "threshold_10pct": 80.0,
  "vi_minus_1": {
    "mapBased": {
      "rank": 320,
      "score": 0.300105
    },
    "tokenBased": {
      "rank": 311,
      "score": 0.242424
    },
    "treeBased": {
      "rank": 441,
      "score": 0.292683
    }
  },
  "vi": {
    "mapBased": {
      "rank": 575,
      "score": 0.237177
    },
    "tokenBased": {
      "rank": 324,
      "score": 0.233918
    },
    "treeBased": {
      "rank": 476,
      "score": 0.281116
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 320,
      "vi_rank": 575,
      "delta": -255,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 311,
      "vi_rank": 324,
      "delta": -13,
      "exceeds_10pct": false
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 441,
      "vi_rank": 476,
      "delta": -35,
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
