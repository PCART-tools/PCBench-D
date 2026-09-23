# 一、突变情况分析

- **Total**: 96
- **替代API**: `networkx.utils.misc.dict_to_numpy_array`
- **10% 阈值**: 9.6

## Vi-1 (networkx-2.7.1-networkx-3.5)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 22 | 0.3052 |
| tokenBased | 39 | 0.2636 |
| treeBased | 56 | 0.3089 |

## Vi (networkx-2.7.1-networkx-3.6)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 27 | 0.3052 |
| tokenBased | 43 | 0.2636 |
| treeBased | 66 | 0.3089 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 22 | 27 | -5 | false |
| tokenBased | 39 | 43 | -4 | false |
| treeBased | 56 | 66 | -10 | true |

```json
{
  "total": 96,
  "replacement_api": "networkx.utils.misc.dict_to_numpy_array",
  "threshold_10pct": 9.6,
  "vi_minus_1": {
    "mapBased": {
      "rank": 22,
      "score": 0.305195
    },
    "tokenBased": {
      "rank": 39,
      "score": 0.263636
    },
    "treeBased": {
      "rank": 56,
      "score": 0.308943
    }
  },
  "vi": {
    "mapBased": {
      "rank": 27,
      "score": 0.305195
    },
    "tokenBased": {
      "rank": 43,
      "score": 0.263636
    },
    "treeBased": {
      "rank": 66,
      "score": 0.308943
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 22,
      "vi_rank": 27,
      "delta": -5,
      "exceeds_10pct": false
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 39,
      "vi_rank": 43,
      "delta": -4,
      "exceeds_10pct": false
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 56,
      "vi_rank": 66,
      "delta": -10,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `R_candidates/Vi-1_networkx-3.5/networkx.utils.misc.dict_to_numpy_array.py`
- **new**: `R_candidates/Vi_networkx-3.6/networkx.utils.misc.dict_to_numpy_array.py`
- **+0 / -0**

```diff
```

```json
{
  "old_file": "R_candidates/Vi-1_networkx-3.5/networkx.utils.misc.dict_to_numpy_array.py",
  "new_file": "R_candidates/Vi_networkx-3.6/networkx.utils.misc.dict_to_numpy_array.py",
  "lines_added": 0,
  "lines_removed": 0
}
```
