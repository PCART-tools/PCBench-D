# 一、突变情况分析

- **Total**: 89
- **替代API**: `networkx.utils.misc.dict_to_numpy_array`
- **10% 阈值**: 8.9

## Vi-1 (networkx-2.7.1-networkx-2.8.8)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 20 | 0.3052 |
| tokenBased | 27 | 0.2636 |
| treeBased | 50 | 0.3089 |

## Vi (networkx-2.7.1-networkx-3.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 17 | 0.3052 |
| tokenBased | 23 | 0.2636 |
| treeBased | 39 | 0.3089 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 20 | 17 | +3 | false |
| tokenBased | 27 | 23 | +4 | false |
| treeBased | 50 | 39 | +11 | true |

```json
{
  "total": 89,
  "replacement_api": "networkx.utils.misc.dict_to_numpy_array",
  "threshold_10pct": 8.9,
  "vi_minus_1": {
    "mapBased": {
      "rank": 20,
      "score": 0.305195
    },
    "tokenBased": {
      "rank": 27,
      "score": 0.263636
    },
    "treeBased": {
      "rank": 50,
      "score": 0.308943
    }
  },
  "vi": {
    "mapBased": {
      "rank": 17,
      "score": 0.305195
    },
    "tokenBased": {
      "rank": 23,
      "score": 0.263636
    },
    "treeBased": {
      "rank": 39,
      "score": 0.308943
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 20,
      "vi_rank": 17,
      "delta": 3,
      "exceeds_10pct": false
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 27,
      "vi_rank": 23,
      "delta": 4,
      "exceeds_10pct": false
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 50,
      "vi_rank": 39,
      "delta": 11,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `R_candidates/Vi-1_networkx-2.8.8/networkx.utils.misc.dict_to_numpy_array.py`
- **new**: `R_candidates/Vi_networkx-3.0/networkx.utils.misc.dict_to_numpy_array.py`
- **+0 / -0**

```diff
```

```json
{
  "old_file": "R_candidates/Vi-1_networkx-2.8.8/networkx.utils.misc.dict_to_numpy_array.py",
  "new_file": "R_candidates/Vi_networkx-3.0/networkx.utils.misc.dict_to_numpy_array.py",
  "lines_added": 0,
  "lines_removed": 0
}
```
