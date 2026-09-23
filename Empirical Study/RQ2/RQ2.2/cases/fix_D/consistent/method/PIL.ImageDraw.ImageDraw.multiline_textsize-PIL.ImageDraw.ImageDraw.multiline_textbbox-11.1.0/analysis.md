# 一、突变情况分析

- **Total**: 803
- **替代API**: `PIL.ImageDraw.ImageDraw.multiline_textbbox`
- **10% 阈值**: 80.3

## Vi-1 (9.5.0-11.1.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 275 | 0.2830 |
| tokenBased | 349 | 0.1869 |
| treeBased | 461 | 0.2687 |

## Vi (9.5.0-11.2.1)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 51 | 0.3913 |
| tokenBased | 207 | 0.2679 |
| treeBased | 139 | 0.3821 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 275 | 51 | +224 | true |
| tokenBased | 349 | 207 | +142 | true |
| treeBased | 461 | 139 | +322 | true |

```json
{
  "total": 803,
  "replacement_api": "PIL.ImageDraw.ImageDraw.multiline_textbbox",
  "threshold_10pct": 80.3,
  "vi_minus_1": {
    "mapBased": {
      "rank": 275,
      "score": 0.28303
    },
    "tokenBased": {
      "rank": 349,
      "score": 0.186937
    },
    "treeBased": {
      "rank": 461,
      "score": 0.268714
    }
  },
  "vi": {
    "mapBased": {
      "rank": 51,
      "score": 0.391328
    },
    "tokenBased": {
      "rank": 207,
      "score": 0.267925
    },
    "treeBased": {
      "rank": 139,
      "score": 0.38206
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 275,
      "vi_rank": 51,
      "delta": 224,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 349,
      "vi_rank": 207,
      "delta": 142,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 461,
      "vi_rank": 139,
      "delta": 322,
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
