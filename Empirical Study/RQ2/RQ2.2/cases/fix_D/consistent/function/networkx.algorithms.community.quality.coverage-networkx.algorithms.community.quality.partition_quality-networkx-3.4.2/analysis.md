# 一、突变情况分析

- **Total**: 107
- **替代API**: `networkx.algorithms.community.quality.partition_quality`
- **10% 阈值**: 10.7

## Vi-1 (networkx-2.5.1-networkx-3.4.2)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 52 | 0.3771 |
| tokenBased | 73 | 0.1364 |
| treeBased | 72 | 0.2126 |

## Vi (networkx-2.5.1-networkx-3.5)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 67 | 0.3771 |
| tokenBased | 93 | 0.1364 |
| treeBased | 92 | 0.2126 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 52 | 67 | -15 | true |
| tokenBased | 73 | 93 | -20 | true |
| treeBased | 72 | 92 | -20 | true |

```json
{
  "total": 107,
  "replacement_api": "networkx.algorithms.community.quality.partition_quality",
  "threshold_10pct": 10.7,
  "vi_minus_1": {
    "mapBased": {
      "rank": 52,
      "score": 0.37706
    },
    "tokenBased": {
      "rank": 73,
      "score": 0.136364
    },
    "treeBased": {
      "rank": 72,
      "score": 0.212644
    }
  },
  "vi": {
    "mapBased": {
      "rank": 67,
      "score": 0.37706
    },
    "tokenBased": {
      "rank": 93,
      "score": 0.136364
    },
    "treeBased": {
      "rank": 92,
      "score": 0.212644
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 52,
      "vi_rank": 67,
      "delta": -15,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 73,
      "vi_rank": 93,
      "delta": -20,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 72,
      "vi_rank": 92,
      "delta": -20,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `R_candidates/Vi-1_networkx-3.4.2/networkx.algorithms.community.quality.partition_quality.py`
- **new**: `R_candidates/Vi_networkx-3.5/networkx.algorithms.community.quality.partition_quality.py`
- **+0 / -0**

```diff
```

```json
{
  "old_file": "R_candidates/Vi-1_networkx-3.4.2/networkx.algorithms.community.quality.partition_quality.py",
  "new_file": "R_candidates/Vi_networkx-3.5/networkx.algorithms.community.quality.partition_quality.py",
  "lines_added": 0,
  "lines_removed": 0
}
```
