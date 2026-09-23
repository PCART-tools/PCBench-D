# 一、突变情况分析

- **Total**: 512
- **替代API**: `pandas.core.arrays.base.ExtensionArray._formatter`
- **10% 阈值**: 51.2

## Vi-1 (v0.23.4-v0.24.2)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 227 | 0.5757 |
| tokenBased | 181 | 0.2400 |
| treeBased | 217 | 0.5556 |

## Vi (v0.23.4-v0.25.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 233 | 0.5757 |
| tokenBased | 324 | 0.1622 |
| treeBased | 296 | 0.3889 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 227 | 233 | -6 | false |
| tokenBased | 181 | 324 | -143 | true |
| treeBased | 217 | 296 | -79 | true |

```json
{
  "total": 512,
  "replacement_api": "pandas.core.arrays.base.ExtensionArray._formatter",
  "threshold_10pct": 51.2,
  "vi_minus_1": {
    "mapBased": {
      "rank": 227,
      "score": 0.575697
    },
    "tokenBased": {
      "rank": 181,
      "score": 0.24
    },
    "treeBased": {
      "rank": 217,
      "score": 0.555556
    }
  },
  "vi": {
    "mapBased": {
      "rank": 233,
      "score": 0.575697
    },
    "tokenBased": {
      "rank": 324,
      "score": 0.162162
    },
    "treeBased": {
      "rank": 296,
      "score": 0.388889
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 227,
      "vi_rank": 233,
      "delta": -6,
      "exceeds_10pct": false
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 181,
      "vi_rank": 324,
      "delta": -143,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 217,
      "vi_rank": 296,
      "delta": -79,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `R_candidates/Vi-1_v0.24.2/pandas.core.arrays.base.ExtensionArray._formatter.py`
- **new**: `R_candidates/Vi_v0.25.0/pandas.core.arrays.base.ExtensionArray._formatter.py`
- **+1 / -2**

```diff
--- R_candidates/Vi-1_v0.24.2/pandas.core.arrays.base.ExtensionArray._formatter.py
+++ R_candidates/Vi_v0.25.0/pandas.core.arrays.base.ExtensionArray._formatter.py
@@ -1,5 +1,4 @@
-    def _formatter(self, boxed=False):
-
+    def _formatter(self, boxed: bool = False) -> Callable[[Any], Optional[str]]:
         
         if boxed:
             return str
```

```json
{
  "old_file": "R_candidates/Vi-1_v0.24.2/pandas.core.arrays.base.ExtensionArray._formatter.py",
  "new_file": "R_candidates/Vi_v0.25.0/pandas.core.arrays.base.ExtensionArray._formatter.py",
  "lines_added": 1,
  "lines_removed": 2
}
```
