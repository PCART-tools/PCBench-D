# 一、突变情况分析

- **Total**: 566
- **替代API**: `pandas.core.indexes.multi.MultiIndex.is_monotonic_increasing`
- **10% 阈值**: 56.6

## Vi-1 (v1.4.4-v2.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 389 | 0.3175 |
| tokenBased | 270 | 0.2021 |
| treeBased | 417 | 0.2818 |

## Vi (v1.5.0-v2.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 389 | 0.3175 |
| tokenBased | 203 | 0.2316 |
| treeBased | 409 | 0.3009 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 389 | 389 | +0 | false |
| tokenBased | 270 | 203 | +67 | true |
| treeBased | 417 | 409 | +8 | false |

```json
{
  "total": 566,
  "replacement_api": "pandas.core.indexes.multi.MultiIndex.is_monotonic_increasing",
  "threshold_10pct": 56.6,
  "vi_minus_1": {
    "mapBased": {
      "rank": 389,
      "score": 0.317452
    },
    "tokenBased": {
      "rank": 270,
      "score": 0.202128
    },
    "treeBased": {
      "rank": 417,
      "score": 0.281818
    }
  },
  "vi": {
    "mapBased": {
      "rank": 389,
      "score": 0.317452
    },
    "tokenBased": {
      "rank": 203,
      "score": 0.231579
    },
    "treeBased": {
      "rank": 409,
      "score": 0.300885
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 389,
      "vi_rank": 389,
      "delta": 0,
      "exceeds_10pct": false
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 270,
      "vi_rank": 203,
      "delta": 67,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 417,
      "vi_rank": 409,
      "delta": 8,
      "exceeds_10pct": false
    }
  ]
}
```

# 二、old → new Diff

- **old**: `pandas.core.indexes.multi.MultiIndex.is_lexsorted/Vi-1_v1.4.4.py`
- **new**: `pandas.core.indexes.multi.MultiIndex.is_lexsorted/Vi_v1.5.0.py`
- **+1 / -1**

```diff
--- pandas.core.indexes.multi.MultiIndex.is_lexsorted/Vi-1_v1.4.4.py
+++ pandas.core.indexes.multi.MultiIndex.is_lexsorted/Vi_v1.5.0.py
@@ -3,6 +3,6 @@
             "MultiIndex.is_lexsorted is deprecated as a public function, "
             "users should use MultiIndex.is_monotonic_increasing instead.",
             FutureWarning,
-            stacklevel=find_stack_level(),
+            stacklevel=find_stack_level(inspect.currentframe()),
         )
         return self._is_lexsorted()
```

```json
{
  "old_file": "pandas.core.indexes.multi.MultiIndex.is_lexsorted/Vi-1_v1.4.4.py",
  "new_file": "pandas.core.indexes.multi.MultiIndex.is_lexsorted/Vi_v1.5.0.py",
  "lines_added": 1,
  "lines_removed": 1
}
```
