# 一、突变情况分析

- **Total**: 1421
- **替代API**: `pandas.core.generic.NDFrame.fillna`
- **10% 阈值**: 142.1

## Vi-1 (v0.12.0-v0.16.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 957 | 0.2617 |
| tokenBased | 576 | 0.2571 |
| treeBased | 662 | 0.3460 |

## Vi (v0.12.0-v0.16.1)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 1175 | 0.2504 |
| tokenBased | 606 | 0.2564 |
| treeBased | 729 | 0.3412 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 957 | 1175 | -218 | true |
| tokenBased | 576 | 606 | -30 | false |
| treeBased | 662 | 729 | -67 | false |

```json
{
  "total": 1421,
  "replacement_api": "pandas.core.generic.NDFrame.fillna",
  "threshold_10pct": 142.1,
  "vi_minus_1": {
    "mapBased": {
      "rank": 957,
      "score": 0.261652
    },
    "tokenBased": {
      "rank": 576,
      "score": 0.257143
    },
    "treeBased": {
      "rank": 662,
      "score": 0.346
    }
  },
  "vi": {
    "mapBased": {
      "rank": 1175,
      "score": 0.250381
    },
    "tokenBased": {
      "rank": 606,
      "score": 0.25641
    },
    "treeBased": {
      "rank": 729,
      "score": 0.341223
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 957,
      "vi_rank": 1175,
      "delta": -218,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 576,
      "vi_rank": 606,
      "delta": -30,
      "exceeds_10pct": false
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 662,
      "vi_rank": 729,
      "delta": -67,
      "exceeds_10pct": false
    }
  ]
}
```

# 二、old → new Diff

- **old**: `R_candidates/Vi-1_v0.16.0/pandas.core.generic.NDFrame.fillna.py`
- **new**: `R_candidates/Vi_v0.16.1/pandas.core.generic.NDFrame.fillna.py`
- **+1 / -1**

```diff
--- R_candidates/Vi-1_v0.16.0/pandas.core.generic.NDFrame.fillna.py
+++ R_candidates/Vi_v0.16.1/pandas.core.generic.NDFrame.fillna.py
@@ -1,6 +1,6 @@
+    @Appender(_shared_docs['fillna'] % _shared_doc_kwargs)
     def fillna(self, value=None, method=None, axis=None, inplace=False,
                limit=None, downcast=None):
-        
         if isinstance(value, (list, tuple)):
             raise TypeError('"value" parameter must be a scalar or dict, but '
                             'you passed a "{0}"'.format(type(value).__name__))
```

```json
{
  "old_file": "R_candidates/Vi-1_v0.16.0/pandas.core.generic.NDFrame.fillna.py",
  "new_file": "R_candidates/Vi_v0.16.1/pandas.core.generic.NDFrame.fillna.py",
  "lines_added": 1,
  "lines_removed": 1
}
```
