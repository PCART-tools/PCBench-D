# 一、突变情况分析

- **Total**: 430
- **替代API**: `polars.series.string.StringNameSpace.count_matches`
- **10% 阈值**: 43.0

## Vi-1 (py-0.19.1-py-1.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 71 | 0.8931 |
| tokenBased | 7 | 0.4118 |
| treeBased | 194 | 0.7083 |

## Vi (py-0.19.2-py-1.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 71 | 0.8931 |
| tokenBased | 1 | 0.6471 |
| treeBased | 17 | 0.8077 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 71 | 71 | +0 | false |
| tokenBased | 7 | 1 | +6 | false |
| treeBased | 194 | 17 | +177 | true |

```json
{
  "total": 430,
  "replacement_api": "polars.series.string.StringNameSpace.count_matches",
  "threshold_10pct": 43.0,
  "vi_minus_1": {
    "mapBased": {
      "rank": 71,
      "score": 0.893082
    },
    "tokenBased": {
      "rank": 7,
      "score": 0.411765
    },
    "treeBased": {
      "rank": 194,
      "score": 0.708333
    }
  },
  "vi": {
    "mapBased": {
      "rank": 71,
      "score": 0.893082
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.647059
    },
    "treeBased": {
      "rank": 17,
      "score": 0.807692
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 71,
      "vi_rank": 71,
      "delta": 0,
      "exceeds_10pct": false
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 7,
      "vi_rank": 1,
      "delta": 6,
      "exceeds_10pct": false
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 194,
      "vi_rank": 17,
      "delta": 177,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `polars.series.string.StringNameSpace.count_match/Vi-1_py-0.19.1.py`
- **new**: `polars.series.string.StringNameSpace.count_match/Vi_py-0.19.2.py`
- **+1 / -1**

```diff
--- polars.series.string.StringNameSpace.count_match/Vi-1_py-0.19.1.py
+++ polars.series.string.StringNameSpace.count_match/Vi_py-0.19.2.py
@@ -1,2 +1,2 @@
-    def count_match(self, pattern: str) -> Series:
+    def count_match(self, pattern: str | Series) -> Series:
         
```

```json
{
  "old_file": "polars.series.string.StringNameSpace.count_match/Vi-1_py-0.19.1.py",
  "new_file": "polars.series.string.StringNameSpace.count_match/Vi_py-0.19.2.py",
  "lines_added": 1,
  "lines_removed": 1
}
```
