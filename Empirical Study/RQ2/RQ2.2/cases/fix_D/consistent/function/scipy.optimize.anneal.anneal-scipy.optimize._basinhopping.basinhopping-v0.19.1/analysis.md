# 一、突变情况分析

- **Total**: 308
- **替代API**: `scipy.optimize._basinhopping.basinhopping`
- **10% 阈值**: 30.8

## Vi-1 (v0.13.3-v0.19.1)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 123 | 0.2644 |
| tokenBased | 116 | 0.2236 |
| treeBased | 35 | 0.3877 |

## Vi (v0.13.3-v1.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 141 | 0.2644 |
| tokenBased | 152 | 0.2236 |
| treeBased | 39 | 0.3877 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 123 | 141 | -18 | false |
| tokenBased | 116 | 152 | -36 | true |
| treeBased | 35 | 39 | -4 | false |

```json
{
  "total": 308,
  "replacement_api": "scipy.optimize._basinhopping.basinhopping",
  "threshold_10pct": 30.8,
  "vi_minus_1": {
    "mapBased": {
      "rank": 123,
      "score": 0.2644
    },
    "tokenBased": {
      "rank": 116,
      "score": 0.223602
    },
    "treeBased": {
      "rank": 35,
      "score": 0.387665
    }
  },
  "vi": {
    "mapBased": {
      "rank": 141,
      "score": 0.2644
    },
    "tokenBased": {
      "rank": 152,
      "score": 0.223602
    },
    "treeBased": {
      "rank": 39,
      "score": 0.387665
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 123,
      "vi_rank": 141,
      "delta": -18,
      "exceeds_10pct": false
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 116,
      "vi_rank": 152,
      "delta": -36,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 35,
      "vi_rank": 39,
      "delta": -4,
      "exceeds_10pct": false
    }
  ]
}
```

# 二、old → new Diff

- **old**: `R_candidates/Vi-1_v0.19.1/scipy.optimize._basinhopping.basinhopping.py`
- **new**: `R_candidates/Vi_v1.0.0/scipy.optimize._basinhopping.basinhopping.py`
- **+0 / -0**

```diff
```

```json
{
  "old_file": "R_candidates/Vi-1_v0.19.1/scipy.optimize._basinhopping.basinhopping.py",
  "new_file": "R_candidates/Vi_v1.0.0/scipy.optimize._basinhopping.basinhopping.py",
  "lines_added": 0,
  "lines_removed": 0
}
```
