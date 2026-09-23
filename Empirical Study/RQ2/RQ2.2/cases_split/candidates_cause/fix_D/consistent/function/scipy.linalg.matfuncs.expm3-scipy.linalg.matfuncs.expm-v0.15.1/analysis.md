# 一、突变情况分析

- **Total**: 244
- **替代API**: `scipy.linalg.matfuncs.expm`
- **10% 阈值**: 24.4

## Vi-1 (v0.12.1-v0.15.1)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 147 | 0.3482 |
| tokenBased | 153 | 0.2340 |
| treeBased | 139 | 0.3613 |

## Vi (v0.12.1-v0.16.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 164 | 0.3482 |
| tokenBased | 192 | 0.2340 |
| treeBased | 165 | 0.3613 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 147 | 164 | -17 | false |
| tokenBased | 153 | 192 | -39 | true |
| treeBased | 139 | 165 | -26 | true |

```json
{
  "total": 244,
  "replacement_api": "scipy.linalg.matfuncs.expm",
  "threshold_10pct": 24.4,
  "vi_minus_1": {
    "mapBased": {
      "rank": 147,
      "score": 0.348214
    },
    "tokenBased": {
      "rank": 153,
      "score": 0.234043
    },
    "treeBased": {
      "rank": 139,
      "score": 0.361345
    }
  },
  "vi": {
    "mapBased": {
      "rank": 164,
      "score": 0.348214
    },
    "tokenBased": {
      "rank": 192,
      "score": 0.234043
    },
    "treeBased": {
      "rank": 165,
      "score": 0.361345
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 147,
      "vi_rank": 164,
      "delta": -17,
      "exceeds_10pct": false
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 153,
      "vi_rank": 192,
      "delta": -39,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 139,
      "vi_rank": 165,
      "delta": -26,
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
