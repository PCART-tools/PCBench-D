# 一、突变情况分析

- **Total**: 68
- **替代API**: `networkx.algorithms.community.quality.partition_quality`
- **10% 阈值**: 6.8

## Vi-1 (networkx-2.5.1-networkx-2.6.2)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 35 | 0.3771 |
| tokenBased | 52 | 0.1373 |
| treeBased | 51 | 0.2151 |

## Vi (networkx-2.5.1-networkx-2.6.3)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 44 | 0.3771 |
| tokenBased | 56 | 0.1373 |
| treeBased | 55 | 0.2151 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 35 | 44 | -9 | true |
| tokenBased | 52 | 56 | -4 | false |
| treeBased | 51 | 55 | -4 | false |

```json
{
  "total": 68,
  "replacement_api": "networkx.algorithms.community.quality.partition_quality",
  "threshold_10pct": 6.8,
  "vi_minus_1": {
    "mapBased": {
      "rank": 35,
      "score": 0.37706
    },
    "tokenBased": {
      "rank": 52,
      "score": 0.137255
    },
    "treeBased": {
      "rank": 51,
      "score": 0.215116
    }
  },
  "vi": {
    "mapBased": {
      "rank": 44,
      "score": 0.37706
    },
    "tokenBased": {
      "rank": 56,
      "score": 0.137255
    },
    "treeBased": {
      "rank": 55,
      "score": 0.215116
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 35,
      "vi_rank": 44,
      "delta": -9,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 52,
      "vi_rank": 56,
      "delta": -4,
      "exceeds_10pct": false
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 51,
      "vi_rank": 55,
      "delta": -4,
      "exceeds_10pct": false
    }
  ]
}
```

# 二、old → new Diff

- **old**: `R_candidates/Vi-1_networkx-2.6.2/networkx.algorithms.community.quality.partition_quality.py`
- **new**: `R_candidates/Vi_networkx-2.6.3/networkx.algorithms.community.quality.partition_quality.py`
- **+0 / -0**

```diff
```

```json
{
  "old_file": "R_candidates/Vi-1_networkx-2.6.2/networkx.algorithms.community.quality.partition_quality.py",
  "new_file": "R_candidates/Vi_networkx-2.6.3/networkx.algorithms.community.quality.partition_quality.py",
  "lines_added": 0,
  "lines_removed": 0
}
```
