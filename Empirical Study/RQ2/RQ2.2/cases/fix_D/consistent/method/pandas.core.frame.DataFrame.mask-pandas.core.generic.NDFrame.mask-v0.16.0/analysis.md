# 一、突变情况分析

- **Total**: 1421
- **替代API**: `pandas.core.generic.NDFrame.mask`
- **10% 阈值**: 142.1

## Vi-1 (v0.12.0-v0.16.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 1 | 1.0000 |
| tokenBased | 1 | 0.9333 |
| treeBased | 1 | 0.9310 |

## Vi (v0.12.0-v0.16.1)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 664 | 0.5450 |
| tokenBased | 60 | 0.4242 |
| treeBased | 813 | 0.3913 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 1 | 664 | -663 | true |
| tokenBased | 1 | 60 | -59 | false |
| treeBased | 1 | 813 | -812 | true |

```json
{
  "total": 1421,
  "replacement_api": "pandas.core.generic.NDFrame.mask",
  "threshold_10pct": 142.1,
  "vi_minus_1": {
    "mapBased": {
      "rank": 1,
      "score": 1.0
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.933333
    },
    "treeBased": {
      "rank": 1,
      "score": 0.931034
    }
  },
  "vi": {
    "mapBased": {
      "rank": 664,
      "score": 0.544959
    },
    "tokenBased": {
      "rank": 60,
      "score": 0.424242
    },
    "treeBased": {
      "rank": 813,
      "score": 0.391304
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 1,
      "vi_rank": 664,
      "delta": -663,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 1,
      "vi_rank": 60,
      "delta": -59,
      "exceeds_10pct": false
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 1,
      "vi_rank": 813,
      "delta": -812,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `R_candidates/Vi-1_v0.16.0/pandas.core.generic.NDFrame.mask.py`
- **new**: `R_candidates/Vi_v0.16.1/pandas.core.generic.NDFrame.mask.py`
- **+5 / -3**

```diff
--- R_candidates/Vi-1_v0.16.0/pandas.core.generic.NDFrame.mask.py
+++ R_candidates/Vi_v0.16.1/pandas.core.generic.NDFrame.mask.py
@@ -1,3 +1,5 @@
-    def mask(self, cond):
-        
-        return self.where(~cond, np.nan)
+    @Appender(_shared_docs['where'] % dict(_shared_doc_kwargs, cond="False"))
+    def mask(self, cond, other=np.nan, inplace=False, axis=None, level=None,
+             try_cast=False, raise_on_error=True):
+        return self.where(~cond, other=other, inplace=inplace, axis=axis,
+            level=level, try_cast=try_cast, raise_on_error=raise_on_error)
```

```json
{
  "old_file": "R_candidates/Vi-1_v0.16.0/pandas.core.generic.NDFrame.mask.py",
  "new_file": "R_candidates/Vi_v0.16.1/pandas.core.generic.NDFrame.mask.py",
  "lines_added": 5,
  "lines_removed": 3
}
```
