# 一、突变情况分析

- **Total**: 822
- **替代API**: `PIL.ImageFont.FreeTypeFont.getlength`
- **10% 阈值**: 82.2

## Vi-1 (9.5.0-10.4.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 7 | 0.7159 |
| tokenBased | 63 | 0.3289 |
| treeBased | 1 | 0.5876 |

## Vi (9.5.0-11.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 7 | 0.7159 |
| tokenBased | 235 | 0.2315 |
| treeBased | 6 | 0.5229 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 7 | 7 | +0 | false |
| tokenBased | 63 | 235 | -172 | true |
| treeBased | 1 | 6 | -5 | false |

```json
{
  "total": 822,
  "replacement_api": "PIL.ImageFont.FreeTypeFont.getlength",
  "threshold_10pct": 82.2,
  "vi_minus_1": {
    "mapBased": {
      "rank": 7,
      "score": 0.71593
    },
    "tokenBased": {
      "rank": 63,
      "score": 0.328947
    },
    "treeBased": {
      "rank": 1,
      "score": 0.587629
    }
  },
  "vi": {
    "mapBased": {
      "rank": 7,
      "score": 0.71593
    },
    "tokenBased": {
      "rank": 235,
      "score": 0.231481
    },
    "treeBased": {
      "rank": 6,
      "score": 0.522936
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 7,
      "vi_rank": 7,
      "delta": 0,
      "exceeds_10pct": false
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 63,
      "vi_rank": 235,
      "delta": -172,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 1,
      "vi_rank": 6,
      "delta": -5,
      "exceeds_10pct": false
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
