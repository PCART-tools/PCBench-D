# 一、突变情况分析

- **Total**: 2702
- **替代API**: `pandas.core.frame.DataFrame.reindex`
- **10% 阈值**: 270.2

## Vi-1 (v0.20.3-v1.0.1)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 884 | 0.4432 |
| tokenBased | 81 | 0.3971 |
| treeBased | 432 | 0.4122 |

## Vi (v0.20.3-v1.0.2)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 1156 | 0.4192 |
| tokenBased | 62 | 0.4154 |
| treeBased | 422 | 0.4141 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 884 | 1156 | -272 | true |
| tokenBased | 81 | 62 | +19 | false |
| treeBased | 432 | 422 | +10 | false |

```json
{
  "total": 2702,
  "replacement_api": "pandas.core.frame.DataFrame.reindex",
  "threshold_10pct": 270.2,
  "vi_minus_1": {
    "mapBased": {
      "rank": 884,
      "score": 0.443182
    },
    "tokenBased": {
      "rank": 81,
      "score": 0.397059
    },
    "treeBased": {
      "rank": 432,
      "score": 0.412214
    }
  },
  "vi": {
    "mapBased": {
      "rank": 1156,
      "score": 0.419231
    },
    "tokenBased": {
      "rank": 62,
      "score": 0.415385
    },
    "treeBased": {
      "rank": 422,
      "score": 0.414062
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 884,
      "vi_rank": 1156,
      "delta": -272,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 81,
      "vi_rank": 62,
      "delta": 19,
      "exceeds_10pct": false
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 432,
      "vi_rank": 422,
      "delta": 10,
      "exceeds_10pct": false
    }
  ]
}
```

# 二、old → new Diff

- **old**: `R_candidates/Vi-1_v1.0.1/pandas.core.frame.DataFrame.reindex.py`
- **new**: `R_candidates/Vi_v1.0.2/pandas.core.frame.DataFrame.reindex.py`
- **+1 / -1**

```diff
--- R_candidates/Vi-1_v1.0.1/pandas.core.frame.DataFrame.reindex.py
+++ R_candidates/Vi_v1.0.2/pandas.core.frame.DataFrame.reindex.py
@@ -17,4 +17,4 @@
 
         kwargs.pop("axis", None)
         kwargs.pop("labels", None)
-        return self._ensure_type(super().reindex(**kwargs))
+        return super().reindex(**kwargs)
```

```json
{
  "old_file": "R_candidates/Vi-1_v1.0.1/pandas.core.frame.DataFrame.reindex.py",
  "new_file": "R_candidates/Vi_v1.0.2/pandas.core.frame.DataFrame.reindex.py",
  "lines_added": 1,
  "lines_removed": 1
}
```
