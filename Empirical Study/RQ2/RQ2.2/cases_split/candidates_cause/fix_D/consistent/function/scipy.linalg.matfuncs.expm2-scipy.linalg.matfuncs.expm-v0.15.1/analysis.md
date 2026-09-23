# 一、突变情况分析

- **Total**: 244
- **替代API**: `scipy.linalg.matfuncs.expm`
- **10% 阈值**: 24.4

## Vi-1 (v0.12.1-v0.15.1)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 161 | 0.3006 |
| tokenBased | 161 | 0.2211 |
| treeBased | 143 | 0.3363 |

## Vi (v0.12.1-v0.16.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 192 | 0.3006 |
| tokenBased | 199 | 0.2211 |
| treeBased | 175 | 0.3363 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 161 | 192 | -31 | true |
| tokenBased | 161 | 199 | -38 | true |
| treeBased | 143 | 175 | -32 | true |

```json
{
  "total": 244,
  "replacement_api": "scipy.linalg.matfuncs.expm",
  "threshold_10pct": 24.4,
  "vi_minus_1": {
    "mapBased": {
      "rank": 161,
      "score": 0.300587
    },
    "tokenBased": {
      "rank": 161,
      "score": 0.221053
    },
    "treeBased": {
      "rank": 143,
      "score": 0.336283
    }
  },
  "vi": {
    "mapBased": {
      "rank": 192,
      "score": 0.300587
    },
    "tokenBased": {
      "rank": 199,
      "score": 0.221053
    },
    "treeBased": {
      "rank": 175,
      "score": 0.336283
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 161,
      "vi_rank": 192,
      "delta": -31,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 161,
      "vi_rank": 199,
      "delta": -38,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 143,
      "vi_rank": 175,
      "delta": -32,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `R_candidates/Vi-1_v0.15.1/scipy.linalg.matfuncs.expm.py`
- **new**: `R_candidates/Vi_v0.16.0/scipy.linalg.matfuncs.expm.py`
- **+0 / -0**

```diff
```

```json
{
  "old_file": "R_candidates/Vi-1_v0.15.1/scipy.linalg.matfuncs.expm.py",
  "new_file": "R_candidates/Vi_v0.16.0/scipy.linalg.matfuncs.expm.py",
  "lines_added": 0,
  "lines_removed": 0
}
```
