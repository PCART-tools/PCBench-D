# 一、突变情况分析

- **Total**: 800
- **替代API**: `PIL.ImageDraw.ImageDraw.multiline_textbbox`
- **10% 阈值**: 80.0

## Vi-1 (9.1.1-10.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 278 | 0.3202 |
| tokenBased | 336 | 0.2246 |
| treeBased | 504 | 0.2779 |

## Vi (9.2.0-10.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 89 | 0.3672 |
| tokenBased | 272 | 0.2530 |
| treeBased | 391 | 0.3142 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 278 | 89 | +189 | true |
| tokenBased | 336 | 272 | +64 | false |
| treeBased | 504 | 391 | +113 | true |

```json
{
  "total": 800,
  "replacement_api": "PIL.ImageDraw.ImageDraw.multiline_textbbox",
  "threshold_10pct": 80.0,
  "vi_minus_1": {
    "mapBased": {
      "rank": 278,
      "score": 0.320175
    },
    "tokenBased": {
      "rank": 336,
      "score": 0.224615
    },
    "treeBased": {
      "rank": 504,
      "score": 0.277904
    }
  },
  "vi": {
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
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 278,
      "vi_rank": 89,
      "delta": 189,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 336,
      "vi_rank": 272,
      "delta": 64,
      "exceeds_10pct": false
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 504,
      "vi_rank": 391,
      "delta": 113,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `PIL.ImageDraw.ImageDraw.multiline_textsize/Vi-1_9.1.1.py`
- **new**: `PIL.ImageDraw.ImageDraw.multiline_textsize/Vi_9.2.0.py`
- **+15 / -8**

```diff
--- PIL.ImageDraw.ImageDraw.multiline_textsize/Vi-1_9.1.1.py
+++ PIL.ImageDraw.ImageDraw.multiline_textsize/Vi_9.2.0.py
@@ -8,14 +8,21 @@
         language=None,
         stroke_width=0,
     ):
+        deprecate("multiline_textsize", 10, "multiline_textbbox")
         max_width = 0
         lines = self._multiline_split(text)
-        line_spacing = (
-            self.textsize("A", font=font, stroke_width=stroke_width)[1] + spacing
-        )
-        for line in lines:
-            line_width, line_height = self.textsize(
-                line, font, spacing, direction, features, language, stroke_width
-            )
-            max_width = max(max_width, line_width)
+        line_spacing = self._multiline_spacing(font, spacing, stroke_width)
+        with warnings.catch_warnings():
+            warnings.filterwarnings("ignore", category=DeprecationWarning)
+            for line in lines:
+                line_width, line_height = self.textsize(
+                    line,
+                    font,
+                    spacing,
+                    direction,
+                    features,
+                    language,
+                    stroke_width,
+                )
+                max_width = max(max_width, line_width)
         return max_width, len(lines) * line_spacing - spacing
```

```json
{
  "old_file": "PIL.ImageDraw.ImageDraw.multiline_textsize/Vi-1_9.1.1.py",
  "new_file": "PIL.ImageDraw.ImageDraw.multiline_textsize/Vi_9.2.0.py",
  "lines_added": 15,
  "lines_removed": 8
}
```
