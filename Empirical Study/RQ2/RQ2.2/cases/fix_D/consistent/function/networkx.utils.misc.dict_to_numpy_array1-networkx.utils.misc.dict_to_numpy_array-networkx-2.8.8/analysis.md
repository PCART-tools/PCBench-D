# 一、突变情况分析

- **Total**: 89
- **替代API**: `networkx.utils.misc.dict_to_numpy_array`
- **10% 阈值**: 8.9

## Vi-1 (networkx-2.7.1-networkx-2.8.8)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 52 | 0.2763 |
| tokenBased | 27 | 0.3214 |
| treeBased | 35 | 0.3978 |

## Vi (networkx-2.7.1-networkx-3.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 38 | 0.2763 |
| tokenBased | 23 | 0.3214 |
| treeBased | 28 | 0.3978 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 52 | 38 | +14 | true |
| tokenBased | 27 | 23 | +4 | false |
| treeBased | 35 | 28 | +7 | false |

```json
{
  "total": 89,
  "replacement_api": "networkx.utils.misc.dict_to_numpy_array",
  "threshold_10pct": 8.9,
  "vi_minus_1": {
    "mapBased": {
      "rank": 52,
      "score": 0.276316
    },
    "tokenBased": {
      "rank": 27,
      "score": 0.321429
    },
    "treeBased": {
      "rank": 35,
      "score": 0.397849
    }
  },
  "vi": {
    "mapBased": {
      "rank": 38,
      "score": 0.276316
    },
    "tokenBased": {
      "rank": 23,
      "score": 0.321429
    },
    "treeBased": {
      "rank": 28,
      "score": 0.397849
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 52,
      "vi_rank": 38,
      "delta": 14,
      "exceeds_10pct": true
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
      "vi1_rank": 35,
      "vi_rank": 28,
      "delta": 7,
      "exceeds_10pct": false
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
