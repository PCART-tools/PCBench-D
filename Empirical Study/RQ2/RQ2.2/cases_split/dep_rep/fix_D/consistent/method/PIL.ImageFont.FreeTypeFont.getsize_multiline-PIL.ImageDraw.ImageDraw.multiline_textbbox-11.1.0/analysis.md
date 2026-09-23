# 一、突变情况分析

- **Total**: 803
- **替代API**: `PIL.ImageDraw.ImageDraw.multiline_textbbox`
- **10% 阈值**: 80.3

## Vi-1 (9.5.0-11.1.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 557 | 0.2284 |
| tokenBased | 386 | 0.1794 |
| treeBased | 522 | 0.2481 |

## Vi (9.5.0-11.2.1)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 91 | 0.3810 |
| tokenBased | 245 | 0.2547 |
| treeBased | 263 | 0.3533 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 557 | 91 | +466 | true |
| tokenBased | 386 | 245 | +141 | true |
| treeBased | 522 | 263 | +259 | true |

```json
{
  "total": 803,
  "replacement_api": "PIL.ImageDraw.ImageDraw.multiline_textbbox",
  "threshold_10pct": 80.3,
  "vi_minus_1": {
    "mapBased": {
      "rank": 557,
      "score": 0.228393
    },
    "tokenBased": {
      "rank": 386,
      "score": 0.179372
    },
    "treeBased": {
      "rank": 522,
      "score": 0.248077
    }
  },
  "vi": {
    "mapBased": {
      "rank": 91,
      "score": 0.381033
    },
    "tokenBased": {
      "rank": 245,
      "score": 0.254682
    },
    "treeBased": {
      "rank": 263,
      "score": 0.353333
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 557,
      "vi_rank": 91,
      "delta": 466,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 386,
      "vi_rank": 245,
      "delta": 141,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 522,
      "vi_rank": 263,
      "delta": 259,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `R_candidates/Vi-1_11.1.0/PIL.ImageDraw.ImageDraw.multiline_textbbox.py`
- **new**: `R_candidates/Vi_11.2.1/PIL.ImageDraw.ImageDraw.multiline_textbbox.py`
- **+16 / -61**

```diff
--- R_candidates/Vi-1_11.1.0/PIL.ImageDraw.ImageDraw.multiline_textbbox.py
+++ R_candidates/Vi_11.2.1/PIL.ImageDraw.ImageDraw.multiline_textbbox.py
@@ -19,69 +19,26 @@
         *,
         font_size: float | None = None,
     ) -> tuple[float, float, float, float]:
-        if direction == "ttb":
-            msg = "ttb direction is unsupported for multiline text"
-            raise ValueError(msg)
-
-        if anchor is None:
-            anchor = "la"
-        elif len(anchor) != 2:
-            msg = "anchor must be a 2 character string"
-            raise ValueError(msg)
-        elif anchor[1] in "tb":
-            msg = "anchor not supported for multiline text"
-            raise ValueError(msg)
-
-        if font is None:
-            font = self._getfont(font_size)
-
-        widths = []
-        max_width: float = 0
-        lines = self._multiline_split(text)
-        line_spacing = self._multiline_spacing(font, spacing, stroke_width)
-        for line in lines:
-            line_width = self.textlength(
-                line,
-                font,
-                direction=direction,
-                features=features,
-                language=language,
-                embedded_color=embedded_color,
-            )
-            widths.append(line_width)
-            max_width = max(max_width, line_width)
-
-        top = xy[1]
-        if anchor[1] == "m":
-            top -= (len(lines) - 1) * line_spacing / 2.0
-        elif anchor[1] == "d":
-            top -= (len(lines) - 1) * line_spacing
+        font, anchor, lines = self._prepare_multiline_text(
+            xy,
+            text,
+            font,
+            anchor,
+            spacing,
+            align,
+            direction,
+            features,
+            language,
+            stroke_width,
+            embedded_color,
+            font_size,
+        )
 
         bbox: tuple[float, float, float, float] | None = None
 
-        for idx, line in enumerate(lines):
-            left = xy[0]
-            width_difference = max_width - widths[idx]
-
-
-            if anchor[0] == "m":
-                left -= width_difference / 2.0
-            elif anchor[0] == "r":
-                left -= width_difference
-
-
-            if align == "left":
-                pass
-            elif align == "center":
-                left += width_difference / 2.0
-            elif align == "right":
-                left += width_difference
-            else:
-                msg = 'align must be "left", "center" or "right"'
-                raise ValueError(msg)
-
+        for xy, line in lines:
             bbox_line = self.textbbox(
-                (left, top),
+                xy,
                 line,
                 font,
                 anchor,
@@ -101,8 +58,6 @@
                     max(bbox[3], bbox_line[3]),
                 )
 
-            top += line_spacing
-
         if bbox is None:
             return xy[0], xy[1], xy[0], xy[1]
         return bbox
```

```json
{
  "old_file": "R_candidates/Vi-1_11.1.0/PIL.ImageDraw.ImageDraw.multiline_textbbox.py",
  "new_file": "R_candidates/Vi_11.2.1/PIL.ImageDraw.ImageDraw.multiline_textbbox.py",
  "lines_added": 16,
  "lines_removed": 61
}
```
