# 一、突变情况分析

- **Total**: 107
- **替代API**: `networkx.algorithms.community.quality.partition_quality`
- **10% 阈值**: 10.7

## Vi-1 (networkx-2.5.1-networkx-3.4.2)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 28 | 0.4534 |
| tokenBased | 26 | 0.2968 |
| treeBased | 54 | 0.3781 |

## Vi (networkx-2.5.1-networkx-3.5)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 32 | 0.4534 |
| tokenBased | 33 | 0.2968 |
| treeBased | 72 | 0.3781 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 28 | 32 | -4 | false |
| tokenBased | 26 | 33 | -7 | false |
| treeBased | 54 | 72 | -18 | true |

```json
{
  "total": 107,
  "replacement_api": "networkx.algorithms.community.quality.partition_quality",
  "threshold_10pct": 10.7,
  "vi_minus_1": {
    "mapBased": {
      "rank": 28,
      "score": 0.453378
    },
    "tokenBased": {
      "rank": 26,
      "score": 0.296774
    },
    "treeBased": {
      "rank": 54,
      "score": 0.378109
    }
  },
  "vi": {
    "mapBased": {
      "rank": 32,
      "score": 0.453378
    },
    "tokenBased": {
      "rank": 33,
      "score": 0.296774
    },
    "treeBased": {
      "rank": 72,
      "score": 0.378109
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 28,
      "vi_rank": 32,
      "delta": -4,
      "exceeds_10pct": false
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 26,
      "vi_rank": 33,
      "delta": -7,
      "exceeds_10pct": false
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 54,
      "vi_rank": 72,
      "delta": -18,
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
