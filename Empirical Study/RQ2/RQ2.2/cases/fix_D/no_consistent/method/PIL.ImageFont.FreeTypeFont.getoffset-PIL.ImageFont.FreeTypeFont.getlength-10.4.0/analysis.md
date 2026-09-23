# 一、突变情况分析

- **Total**: 822
- **替代API**: `PIL.ImageFont.FreeTypeFont.getlength`
- **10% 阈值**: 82.2

## Vi-1 (9.5.0-10.4.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 115 | 0.7035 |
| tokenBased | 287 | 0.2364 |
| treeBased | 142 | 0.5333 |

## Vi (9.5.0-11.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 110 | 0.7035 |
| tokenBased | 556 | 0.1494 |
| treeBased | 308 | 0.4444 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 115 | 110 | +5 | false |
| tokenBased | 287 | 556 | -269 | true |
| treeBased | 142 | 308 | -166 | true |

```json
{
  "total": 822,
  "replacement_api": "PIL.ImageFont.FreeTypeFont.getlength",
  "threshold_10pct": 82.2,
  "vi_minus_1": {
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
  "vi": {
    "mapBased": {
      "rank": 110,
      "score": 0.703534
    },
    "tokenBased": {
      "rank": 556,
      "score": 0.149425
    },
    "treeBased": {
      "rank": 308,
      "score": 0.444444
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 115,
      "vi_rank": 110,
      "delta": 5,
      "exceeds_10pct": false
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 287,
      "vi_rank": 556,
      "delta": -269,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 142,
      "vi_rank": 308,
      "delta": -166,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `R_candidates/Vi-1_10.4.0/PIL.ImageFont.FreeTypeFont.getlength.py`
- **new**: `R_candidates/Vi_11.0.0/PIL.ImageFont.FreeTypeFont.getlength.py`
- **+6 / -1**

```diff
--- R_candidates/Vi-1_10.4.0/PIL.ImageFont.FreeTypeFont.getlength.py
+++ R_candidates/Vi_11.0.0/PIL.ImageFont.FreeTypeFont.getlength.py
@@ -1,5 +1,10 @@
     def getlength(
-        self, text: str | bytes, mode="", direction=None, features=None, language=None
+        self,
+        text: str | bytes,
+        mode: str = "",
+        direction: str | None = None,
+        features: list[str] | None = None,
+        language: str | None = None,
     ) -> float:
         
         _string_length_check(text)
```

```json
{
  "old_file": "R_candidates/Vi-1_10.4.0/PIL.ImageFont.FreeTypeFont.getlength.py",
  "new_file": "R_candidates/Vi_11.0.0/PIL.ImageFont.FreeTypeFont.getlength.py",
  "lines_added": 6,
  "lines_removed": 1
}
```
