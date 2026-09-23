# 一、突变情况分析

- **Total**: 815
- **替代API**: `PIL.ImageFont.FreeTypeFont.getlength`
- **10% 阈值**: 81.5

## Vi-1 (9.5.0-10.3.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 123 | 0.7035 |
| tokenBased | 85 | 0.3171 |
| treeBased | 71 | 0.5893 |

## Vi (9.5.0-10.4.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 115 | 0.7035 |
| tokenBased | 287 | 0.2364 |
| treeBased | 142 | 0.5333 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 123 | 115 | +8 | false |
| tokenBased | 85 | 287 | -202 | true |
| treeBased | 71 | 142 | -71 | false |

```json
{
  "total": 815,
  "replacement_api": "PIL.ImageFont.FreeTypeFont.getlength",
  "threshold_10pct": 81.5,
  "vi_minus_1": {
    "mapBased": {
      "rank": 123,
      "score": 0.703534
    },
    "tokenBased": {
      "rank": 85,
      "score": 0.317073
    },
    "treeBased": {
      "rank": 71,
      "score": 0.589286
    }
  },
  "vi": {
    "mapBased": {
      "rank": 115,
      "score": 0.703534
    },
    "tokenBased": {
      "rank": 287,
      "score": 0.236364
    },
    "treeBased": {
      "rank": 142,
      "score": 0.533333
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 123,
      "vi_rank": 115,
      "delta": 8,
      "exceeds_10pct": false
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 85,
      "vi_rank": 287,
      "delta": -202,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 71,
      "vi_rank": 142,
      "delta": -71,
      "exceeds_10pct": false
    }
  ]
}
```

# 二、old → new Diff

- **old**: `R_candidates/Vi-1_10.3.0/PIL.ImageFont.FreeTypeFont.getlength.py`
- **new**: `R_candidates/Vi_10.4.0/PIL.ImageFont.FreeTypeFont.getlength.py`
- **+3 / -1**

```diff
--- R_candidates/Vi-1_10.3.0/PIL.ImageFont.FreeTypeFont.getlength.py
+++ R_candidates/Vi_10.4.0/PIL.ImageFont.FreeTypeFont.getlength.py
@@ -1,4 +1,6 @@
-    def getlength(self, text, mode="", direction=None, features=None, language=None):
+    def getlength(
+        self, text: str | bytes, mode="", direction=None, features=None, language=None
+    ) -> float:
         
         _string_length_check(text)
         return self.font.getlength(text, mode, direction, features, language) / 64
```

```json
{
  "old_file": "R_candidates/Vi-1_10.3.0/PIL.ImageFont.FreeTypeFont.getlength.py",
  "new_file": "R_candidates/Vi_10.4.0/PIL.ImageFont.FreeTypeFont.getlength.py",
  "lines_added": 3,
  "lines_removed": 1
}
```
