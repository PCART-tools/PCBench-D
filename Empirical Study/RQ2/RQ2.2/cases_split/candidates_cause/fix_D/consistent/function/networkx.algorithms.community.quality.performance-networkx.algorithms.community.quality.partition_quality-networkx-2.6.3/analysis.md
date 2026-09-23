# 一、突变情况分析

- **Total**: 78
- **替代API**: `networkx.algorithms.community.quality.partition_quality`
- **10% 阈值**: 7.8

## Vi-1 (networkx-2.5.1-networkx-2.6.3)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 23 | 0.4534 |
| tokenBased | 18 | 0.2987 |
| treeBased | 41 | 0.3819 |

## Vi (networkx-2.5.1-networkx-2.7)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 28 | 0.4534 |
| tokenBased | 26 | 0.2987 |
| treeBased | 49 | 0.3819 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 23 | 28 | -5 | false |
| tokenBased | 18 | 26 | -8 | true |
| treeBased | 41 | 49 | -8 | true |

```json
{
  "total": 78,
  "replacement_api": "networkx.algorithms.community.quality.partition_quality",
  "threshold_10pct": 7.8,
  "vi_minus_1": {
    "mapBased": {
      "rank": 23,
      "score": 0.453378
    },
    "tokenBased": {
      "rank": 18,
      "score": 0.298701
    },
    "treeBased": {
      "rank": 41,
      "score": 0.38191
    }
  },
  "vi": {
    "mapBased": {
      "rank": 28,
      "score": 0.453378
    },
    "tokenBased": {
      "rank": 26,
      "score": 0.298701
    },
    "treeBased": {
      "rank": 49,
      "score": 0.38191
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 23,
      "vi_rank": 28,
      "delta": -5,
      "exceeds_10pct": false
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 18,
      "vi_rank": 26,
      "delta": -8,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 41,
      "vi_rank": 49,
      "delta": -8,
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
