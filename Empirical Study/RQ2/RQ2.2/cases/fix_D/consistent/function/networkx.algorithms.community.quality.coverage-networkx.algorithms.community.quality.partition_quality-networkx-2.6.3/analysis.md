# 一、突变情况分析

- **Total**: 78
- **替代API**: `networkx.algorithms.community.quality.partition_quality`
- **10% 阈值**: 7.8

## Vi-1 (networkx-2.5.1-networkx-2.6.3)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 44 | 0.3771 |
| tokenBased | 56 | 0.1373 |
| treeBased | 55 | 0.2151 |

## Vi (networkx-2.5.1-networkx-2.7)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 51 | 0.3771 |
| tokenBased | 67 | 0.1373 |
| treeBased | 66 | 0.2151 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 44 | 51 | -7 | false |
| tokenBased | 56 | 67 | -11 | true |
| treeBased | 55 | 66 | -11 | true |

```json
{
  "total": 78,
  "replacement_api": "networkx.algorithms.community.quality.partition_quality",
  "threshold_10pct": 7.8,
  "vi_minus_1": {
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
  "vi": {
    "mapBased": {
      "rank": 51,
      "score": 0.37706
    },
    "tokenBased": {
      "rank": 67,
      "score": 0.137255
    },
    "treeBased": {
      "rank": 66,
      "score": 0.215116
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 44,
      "vi_rank": 51,
      "delta": -7,
      "exceeds_10pct": false
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 56,
      "vi_rank": 67,
      "delta": -11,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 55,
      "vi_rank": 66,
      "delta": -11,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `R_candidates/Vi-1_networkx-2.6.3/networkx.algorithms.community.quality.partition_quality.py`
- **new**: `R_candidates/Vi_networkx-2.7/networkx.algorithms.community.quality.partition_quality.py`
- **+0 / -0**

```diff
```

```json
{
  "old_file": "R_candidates/Vi-1_networkx-2.6.3/networkx.algorithms.community.quality.partition_quality.py",
  "new_file": "R_candidates/Vi_networkx-2.7/networkx.algorithms.community.quality.partition_quality.py",
  "lines_added": 0,
  "lines_removed": 0
}
```
