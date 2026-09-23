# 一、突变情况分析

- **Total**: 89
- **替代API**: `networkx.utils.misc.make_list_of_ints`
- **10% 阈值**: 8.9

## Vi-1 (networkx-2.5.1-networkx-2.8.8)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 29 | 0.3508 |
| tokenBased | 25 | 0.2333 |
| treeBased | 68 | 0.3448 |

## Vi (networkx-2.5.1-networkx-3.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 19 | 0.3508 |
| tokenBased | 13 | 0.2333 |
| treeBased | 46 | 0.3448 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 29 | 19 | +10 | true |
| tokenBased | 25 | 13 | +12 | true |
| treeBased | 68 | 46 | +22 | true |

```json
{
  "total": 89,
  "replacement_api": "networkx.utils.misc.make_list_of_ints",
  "threshold_10pct": 8.9,
  "vi_minus_1": {
    "mapBased": {
      "rank": 29,
      "score": 0.350761
    },
    "tokenBased": {
      "rank": 25,
      "score": 0.233333
    },
    "treeBased": {
      "rank": 68,
      "score": 0.344828
    }
  },
  "vi": {
    "mapBased": {
      "rank": 19,
      "score": 0.350761
    },
    "tokenBased": {
      "rank": 13,
      "score": 0.233333
    },
    "treeBased": {
      "rank": 46,
      "score": 0.344828
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 29,
      "vi_rank": 19,
      "delta": 10,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 25,
      "vi_rank": 13,
      "delta": 12,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 68,
      "vi_rank": 46,
      "delta": 22,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `R_candidates/Vi-1_networkx-2.8.8/networkx.utils.misc.make_list_of_ints.py`
- **new**: `R_candidates/Vi_networkx-3.0/networkx.utils.misc.make_list_of_ints.py`
- **+0 / -0**

```diff
```

```json
{
  "old_file": "R_candidates/Vi-1_networkx-2.8.8/networkx.utils.misc.make_list_of_ints.py",
  "new_file": "R_candidates/Vi_networkx-3.0/networkx.utils.misc.make_list_of_ints.py",
  "lines_added": 0,
  "lines_removed": 0
}
```
