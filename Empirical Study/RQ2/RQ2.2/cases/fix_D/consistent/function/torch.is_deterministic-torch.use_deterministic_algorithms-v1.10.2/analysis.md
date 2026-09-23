# 一、突变情况分析

- **Total**: 6795
- **替代API**: `torch.use_deterministic_algorithms`
- **10% 阈值**: 679.5

## Vi-1 (v1.9.1-v1.10.2)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 404 | 0.6694 |
| tokenBased | 48 | 0.3846 |
| treeBased | 37 | 0.6667 |

## Vi (v1.9.1-v1.11.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 1168 | 0.5786 |
| tokenBased | 115 | 0.3448 |
| treeBased | 707 | 0.5517 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 404 | 1168 | -764 | true |
| tokenBased | 48 | 115 | -67 | false |
| treeBased | 37 | 707 | -670 | false |

```json
{
  "total": 6795,
  "replacement_api": "torch.use_deterministic_algorithms",
  "threshold_10pct": 679.5,
  "vi_minus_1": {
    "mapBased": {
      "rank": 404,
      "score": 0.669379
    },
    "tokenBased": {
      "rank": 48,
      "score": 0.384615
    },
    "treeBased": {
      "rank": 37,
      "score": 0.666667
    }
  },
  "vi": {
    "mapBased": {
      "rank": 1168,
      "score": 0.578608
    },
    "tokenBased": {
      "rank": 115,
      "score": 0.344828
    },
    "treeBased": {
      "rank": 707,
      "score": 0.551724
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 404,
      "vi_rank": 1168,
      "delta": -764,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 48,
      "vi_rank": 115,
      "delta": -67,
      "exceeds_10pct": false
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 37,
      "vi_rank": 707,
      "delta": -670,
      "exceeds_10pct": false
    }
  ]
}
```

# 二、old → new Diff

- **old**: `R_candidates/Vi-1_v1.10.2/torch.use_deterministic_algorithms.py`
- **new**: `R_candidates/Vi_v1.11.0/torch.use_deterministic_algorithms.py`
- **+2 / -2**

```diff
--- R_candidates/Vi-1_v1.10.2/torch.use_deterministic_algorithms.py
+++ R_candidates/Vi_v1.11.0/torch.use_deterministic_algorithms.py
@@ -1,3 +1,3 @@
-def use_deterministic_algorithms(mode):
+def use_deterministic_algorithms(mode, *, warn_only=False):
     
-    _C._set_deterministic_algorithms(mode)
+    _C._set_deterministic_algorithms(mode, warn_only=warn_only)
```

```json
{
  "old_file": "R_candidates/Vi-1_v1.10.2/torch.use_deterministic_algorithms.py",
  "new_file": "R_candidates/Vi_v1.11.0/torch.use_deterministic_algorithms.py",
  "lines_added": 2,
  "lines_removed": 2
}
```
