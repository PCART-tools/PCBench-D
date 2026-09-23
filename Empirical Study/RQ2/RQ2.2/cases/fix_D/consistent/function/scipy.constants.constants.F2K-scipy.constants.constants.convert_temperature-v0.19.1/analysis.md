# 一、突变情况分析

- **Total**: 32
- **替代API**: `scipy.constants.constants.convert_temperature`
- **10% 阈值**: 3.2

## Vi-1 (v0.17.1-v0.19.1)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 28 | 0.2266 |
| tokenBased | 31 | 0.0795 |
| treeBased | 31 | 0.1270 |

## Vi (v0.17.1-v1.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 17 | 0.2266 |
| tokenBased | 19 | 0.0795 |
| treeBased | 19 | 0.1270 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 28 | 17 | +11 | true |
| tokenBased | 31 | 19 | +12 | true |
| treeBased | 31 | 19 | +12 | true |

```json
{
  "total": 32,
  "replacement_api": "scipy.constants.constants.convert_temperature",
  "threshold_10pct": 3.2,
  "vi_minus_1": {
    "mapBased": {
      "rank": 28,
      "score": 0.226584
    },
    "tokenBased": {
      "rank": 31,
      "score": 0.079545
    },
    "treeBased": {
      "rank": 31,
      "score": 0.126984
    }
  },
  "vi": {
    "mapBased": {
      "rank": 17,
      "score": 0.226584
    },
    "tokenBased": {
      "rank": 19,
      "score": 0.079545
    },
    "treeBased": {
      "rank": 19,
      "score": 0.126984
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 28,
      "vi_rank": 17,
      "delta": 11,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 31,
      "vi_rank": 19,
      "delta": 12,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 31,
      "vi_rank": 19,
      "delta": 12,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `R_candidates/Vi-1_v0.19.1/scipy.constants.constants.convert_temperature.py`
- **new**: `R_candidates/Vi_v1.0.0/scipy.constants.constants.convert_temperature.py`
- **+0 / -0**

```diff
```

```json
{
  "old_file": "R_candidates/Vi-1_v0.19.1/scipy.constants.constants.convert_temperature.py",
  "new_file": "R_candidates/Vi_v1.0.0/scipy.constants.constants.convert_temperature.py",
  "lines_added": 0,
  "lines_removed": 0
}
```
