# 一、突变情况分析

- **Total**: 800
- **替代API**: `PIL.ImageFont.FreeTypeFont.getlength`
- **10% 阈值**: 80.0

## Vi-1 (9.1.1-10.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 197 | 0.6367 |
| tokenBased | 281 | 0.2632 |
| treeBased | 300 | 0.5400 |

## Vi (9.2.0-10.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 114 | 0.7035 |
| tokenBased | 133 | 0.3171 |
| treeBased | 118 | 0.5893 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 197 | 114 | +83 | true |
| tokenBased | 281 | 133 | +148 | true |
| treeBased | 300 | 118 | +182 | true |

```json
{
  "total": 800,
  "replacement_api": "PIL.ImageFont.FreeTypeFont.getlength",
  "threshold_10pct": 80.0,
  "vi_minus_1": {
    "mapBased": {
      "rank": 197,
      "score": 0.63674
    },
    "tokenBased": {
      "rank": 281,
      "score": 0.263158
    },
    "treeBased": {
      "rank": 300,
      "score": 0.54
    }
  },
  "vi": {
    "mapBased": {
      "rank": 114,
      "score": 0.703534
    },
    "tokenBased": {
      "rank": 133,
      "score": 0.317073
    },
    "treeBased": {
      "rank": 118,
      "score": 0.589286
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 197,
      "vi_rank": 114,
      "delta": 83,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 281,
      "vi_rank": 133,
      "delta": 148,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 300,
      "vi_rank": 118,
      "delta": 182,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `PIL.ImageFont.FreeTypeFont.getoffset/Vi-1_9.1.1.py`
- **new**: `PIL.ImageFont.FreeTypeFont.getoffset/Vi_9.2.0.py`
- **+1 / -0**

```diff
--- PIL.ImageFont.FreeTypeFont.getoffset/Vi-1_9.1.1.py
+++ PIL.ImageFont.FreeTypeFont.getoffset/Vi_9.2.0.py
@@ -1,3 +1,4 @@
     def getoffset(self, text):
         
+        deprecate("getoffset", 10, "getbbox")
         return self.font.getsize(text)[1]
```

```json
{
  "old_file": "PIL.ImageFont.FreeTypeFont.getoffset/Vi-1_9.1.1.py",
  "new_file": "PIL.ImageFont.FreeTypeFont.getoffset/Vi_9.2.0.py",
  "lines_added": 1,
  "lines_removed": 0
}
```
