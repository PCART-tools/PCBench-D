# 一、突变情况分析

- **Total**: 1231
- **替代API**: `pandas.core.generic.NDFrame.fillna`
- **10% 阈值**: 123.1

## Vi-1 (v0.8.1-v0.13.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 632 | 0.2862 |
| tokenBased | 541 | 0.2712 |
| treeBased | 599 | 0.3448 |

## Vi (v0.9.0-v0.13.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 496 | 0.3065 |
| tokenBased | 471 | 0.2919 |
| treeBased | 477 | 0.3661 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 632 | 496 | +136 | true |
| tokenBased | 541 | 471 | +70 | false |
| treeBased | 599 | 477 | +122 | false |

```json
{
  "total": 1231,
  "replacement_api": "pandas.core.generic.NDFrame.fillna",
  "threshold_10pct": 123.1,
  "vi_minus_1": {
    "mapBased": {
      "rank": 632,
      "score": 0.286196
    },
    "tokenBased": {
      "rank": 541,
      "score": 0.271186
    },
    "treeBased": {
      "rank": 599,
      "score": 0.344828
    }
  },
  "vi": {
    "mapBased": {
      "rank": 496,
      "score": 0.306463
    },
    "tokenBased": {
      "rank": 471,
      "score": 0.291946
    },
    "treeBased": {
      "rank": 477,
      "score": 0.366071
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 632,
      "vi_rank": 496,
      "delta": 136,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 541,
      "vi_rank": 471,
      "delta": 70,
      "exceeds_10pct": false
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 599,
      "vi_rank": 477,
      "delta": 122,
      "exceeds_10pct": false
    }
  ]
}
```

# 二、old → new Diff

- **old**: `pandas.core.series.Series.fillna/Vi-1_v0.8.1.py`
- **new**: `pandas.core.series.Series.fillna/Vi_v0.9.0.py`
- **+3 / -0**

```diff
--- pandas.core.series.Series.fillna/Vi-1_v0.8.1.py
+++ pandas.core.series.Series.fillna/Vi_v0.9.0.py
@@ -2,6 +2,9 @@
     def fillna(self, value=None, method='pad', inplace=False,
                limit=None):
         
+        if not self._can_hold_na:
+            return self.copy() if not inplace else self
+
         if value is not None:
             result = self.copy() if not inplace else self
             mask = isnull(self.values)
```

```json
{
  "old_file": "pandas.core.series.Series.fillna/Vi-1_v0.8.1.py",
  "new_file": "pandas.core.series.Series.fillna/Vi_v0.9.0.py",
  "lines_added": 3,
  "lines_removed": 0
}
```
