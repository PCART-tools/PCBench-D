# 一、突变情况分析

- **Total**: 1231
- **替代API**: `pandas.core.generic.NDFrame.fillna`
- **10% 阈值**: 123.1

## Vi-1 (v0.11.0-v0.13.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 944 | 0.2700 |
| tokenBased | 676 | 0.2371 |
| treeBased | 757 | 0.3325 |

## Vi (v0.12.0-v0.13.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 600 | 0.3201 |
| tokenBased | 437 | 0.3093 |
| treeBased | 417 | 0.4023 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 944 | 600 | +344 | true |
| tokenBased | 676 | 437 | +239 | true |
| treeBased | 757 | 417 | +340 | true |

```json
{
  "total": 1231,
  "replacement_api": "pandas.core.generic.NDFrame.fillna",
  "threshold_10pct": 123.1,
  "vi_minus_1": {
    "mapBased": {
      "rank": 944,
      "score": 0.27002
    },
    "tokenBased": {
      "rank": 676,
      "score": 0.237113
    },
    "treeBased": {
      "rank": 757,
      "score": 0.332524
    }
  },
  "vi": {
    "mapBased": {
      "rank": 600,
      "score": 0.320075
    },
    "tokenBased": {
      "rank": 437,
      "score": 0.309278
    },
    "treeBased": {
      "rank": 417,
      "score": 0.402326
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 944,
      "vi_rank": 600,
      "delta": 344,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 676,
      "vi_rank": 437,
      "delta": 239,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 757,
      "vi_rank": 417,
      "delta": 340,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `pandas.core.panel.Panel.fillna/Vi-1_v0.11.0.py`
- **new**: `pandas.core.panel.Panel.fillna/Vi_v0.12.0.py`
- **+3 / -0**

```diff
--- pandas.core.panel.Panel.fillna/Vi-1_v0.11.0.py
+++ pandas.core.panel.Panel.fillna/Vi_v0.12.0.py
@@ -1,5 +1,8 @@
     def fillna(self, value=None, method=None):
         
+        if isinstance(value, (list, tuple)):
+            raise TypeError('"value" parameter must be a scalar or dict, but '
+                            'you passed a "{0}"'.format(type(value).__name__))
         if value is None:
             if method is None:
                 raise ValueError('must specify a fill method or value')
```

```json
{
  "old_file": "pandas.core.panel.Panel.fillna/Vi-1_v0.11.0.py",
  "new_file": "pandas.core.panel.Panel.fillna/Vi_v0.12.0.py",
  "lines_added": 3,
  "lines_removed": 0
}
```
