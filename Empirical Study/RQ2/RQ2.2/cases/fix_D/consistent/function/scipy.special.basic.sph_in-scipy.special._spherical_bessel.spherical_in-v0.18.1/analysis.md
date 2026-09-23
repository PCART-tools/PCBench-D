# 一、突变情况分析

- **Total**: 303
- **替代API**: `scipy.special._spherical_bessel.spherical_in`
- **10% 阈值**: 30.3

## Vi-1 (v0.17.1-v0.18.1)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 106 | 0.3516 |
| tokenBased | 200 | 0.1863 |
| treeBased | 198 | 0.2906 |

## Vi (v0.17.1-v0.19.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 112 | 0.3516 |
| tokenBased | 252 | 0.1863 |
| treeBased | 246 | 0.2906 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 106 | 112 | -6 | false |
| tokenBased | 200 | 252 | -52 | true |
| treeBased | 198 | 246 | -48 | true |

```json
{
  "total": 303,
  "replacement_api": "scipy.special._spherical_bessel.spherical_in",
  "threshold_10pct": 30.3,
  "vi_minus_1": {
    "mapBased": {
      "rank": 106,
      "score": 0.351598
    },
    "tokenBased": {
      "rank": 200,
      "score": 0.186275
    },
    "treeBased": {
      "rank": 198,
      "score": 0.290598
    }
  },
  "vi": {
    "mapBased": {
      "rank": 112,
      "score": 0.351598
    },
    "tokenBased": {
      "rank": 252,
      "score": 0.186275
    },
    "treeBased": {
      "rank": 246,
      "score": 0.290598
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 106,
      "vi_rank": 112,
      "delta": -6,
      "exceeds_10pct": false
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 200,
      "vi_rank": 252,
      "delta": -52,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 198,
      "vi_rank": 246,
      "delta": -48,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `R_candidates/Vi-1_v0.18.1/scipy.special._spherical_bessel.spherical_in.py`
- **new**: `R_candidates/Vi_v0.19.0/scipy.special._spherical_bessel.spherical_in.py`
- **+0 / -0**

```diff
```

```json
{
  "old_file": "R_candidates/Vi-1_v0.18.1/scipy.special._spherical_bessel.spherical_in.py",
  "new_file": "R_candidates/Vi_v0.19.0/scipy.special._spherical_bessel.spherical_in.py",
  "lines_added": 0,
  "lines_removed": 0
}
```
