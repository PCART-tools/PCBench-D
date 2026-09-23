# 一、突变情况分析

- **Total**: 800
- **替代API**: `PIL.ImageDraw.ImageDraw.multiline_textbbox`
- **10% 阈值**: 80.0

## Vi-1 (9.1.1-10.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 393 | 0.3019 |
| tokenBased | 390 | 0.2092 |
| treeBased | 578 | 0.2569 |

## Vi (9.2.0-10.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 320 | 0.3001 |
| tokenBased | 311 | 0.2424 |
| treeBased | 441 | 0.2927 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 393 | 320 | +73 | false |
| tokenBased | 390 | 311 | +79 | false |
| treeBased | 578 | 441 | +137 | true |

```json
{
  "total": 800,
  "replacement_api": "PIL.ImageDraw.ImageDraw.multiline_textbbox",
  "threshold_10pct": 80.0,
  "vi_minus_1": {
    "mapBased": {
      "rank": 393,
      "score": 0.301881
    },
    "tokenBased": {
      "rank": 390,
      "score": 0.209231
    },
    "treeBased": {
      "rank": 578,
      "score": 0.256944
    }
  },
  "vi": {
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
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 393,
      "vi_rank": 320,
      "delta": 73,
      "exceeds_10pct": false
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 390,
      "vi_rank": 311,
      "delta": 79,
      "exceeds_10pct": false
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 578,
      "vi_rank": 441,
      "delta": 137,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `PIL.ImageFont.FreeTypeFont.getsize_multiline/Vi-1_9.1.1.py`
- **new**: `PIL.ImageFont.FreeTypeFont.getsize_multiline/Vi_9.2.0.py`
- **+9 / -6**

```diff
--- PIL.ImageFont.FreeTypeFont.getsize_multiline/Vi-1_9.1.1.py
+++ PIL.ImageFont.FreeTypeFont.getsize_multiline/Vi_9.2.0.py
@@ -8,13 +8,16 @@
         stroke_width=0,
     ):
         
+        deprecate("getsize_multiline", 10, "ImageDraw.multiline_textbbox")
         max_width = 0
         lines = self._multiline_split(text)
-        line_spacing = self.getsize("A", stroke_width=stroke_width)[1] + spacing
-        for line in lines:
-            line_width, line_height = self.getsize(
-                line, direction, features, language, stroke_width
-            )
-            max_width = max(max_width, line_width)
+        with warnings.catch_warnings():
+            warnings.filterwarnings("ignore", category=DeprecationWarning)
+            line_spacing = self.getsize("A", stroke_width=stroke_width)[1] + spacing
+            for line in lines:
+                line_width, line_height = self.getsize(
+                    line, direction, features, language, stroke_width
+                )
+                max_width = max(max_width, line_width)
 
         return max_width, len(lines) * line_spacing - spacing
```

```json
{
  "old_file": "PIL.ImageFont.FreeTypeFont.getsize_multiline/Vi-1_9.1.1.py",
  "new_file": "PIL.ImageFont.FreeTypeFont.getsize_multiline/Vi_9.2.0.py",
  "lines_added": 9,
  "lines_removed": 6
}
```
