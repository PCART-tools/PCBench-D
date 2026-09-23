# 一、突变情况分析

- **Total**: 248
- **替代API**: `scipy.integrate._quadpack_py.quad`
- **10% 阈值**: 24.8

## Vi-1 (v1.11.4-v1.14.1)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 137 | 0.2470 |
| tokenBased | 149 | 0.1914 |
| treeBased | 187 | 0.2245 |

## Vi (v1.11.4-v1.15.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 161 | 0.2470 |
| tokenBased | 170 | 0.1914 |
| treeBased | 216 | 0.2245 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 137 | 161 | -24 | false |
| tokenBased | 149 | 170 | -21 | false |
| treeBased | 187 | 216 | -29 | true |

```json
{
  "total": 248,
  "replacement_api": "scipy.integrate._quadpack_py.quad",
  "threshold_10pct": 24.8,
  "vi_minus_1": {
    "mapBased": {
      "rank": 137,
      "score": 0.246982
    },
    "tokenBased": {
      "rank": 149,
      "score": 0.191413
    },
    "treeBased": {
      "rank": 187,
      "score": 0.22449
    }
  },
  "vi": {
    "mapBased": {
      "rank": 161,
      "score": 0.246982
    },
    "tokenBased": {
      "rank": 170,
      "score": 0.191413
    },
    "treeBased": {
      "rank": 216,
      "score": 0.22449
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 137,
      "vi_rank": 161,
      "delta": -24,
      "exceeds_10pct": false
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 149,
      "vi_rank": 170,
      "delta": -21,
      "exceeds_10pct": false
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 187,
      "vi_rank": 216,
      "delta": -29,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `R_candidates/Vi-1_v1.14.1/scipy.integrate._quadpack_py.quad.py`
- **new**: `R_candidates/Vi_v1.15.0/scipy.integrate._quadpack_py.quad.py`
- **+0 / -0**

```diff
```

```json
{
  "old_file": "R_candidates/Vi-1_v1.14.1/scipy.integrate._quadpack_py.quad.py",
  "new_file": "R_candidates/Vi_v1.15.0/scipy.integrate._quadpack_py.quad.py",
  "lines_added": 0,
  "lines_removed": 0
}
```
