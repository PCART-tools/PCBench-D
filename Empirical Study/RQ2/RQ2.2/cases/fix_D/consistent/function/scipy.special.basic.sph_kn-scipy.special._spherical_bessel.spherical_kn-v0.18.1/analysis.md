# 一、突变情况分析

- **Total**: 303
- **替代API**: `scipy.special._spherical_bessel.spherical_kn`
- **10% 阈值**: 30.3

## Vi-1 (v0.17.1-v0.18.1)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 106 | 0.3516 |
| tokenBased | 204 | 0.1759 |
| treeBased | 199 | 0.2787 |

## Vi (v0.17.1-v0.19.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 112 | 0.3516 |
| tokenBased | 255 | 0.1759 |
| treeBased | 247 | 0.2787 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 106 | 112 | -6 | false |
| tokenBased | 204 | 255 | -51 | true |
| treeBased | 199 | 247 | -48 | true |

```json
{
  "total": 303,
  "replacement_api": "scipy.special._spherical_bessel.spherical_kn",
  "threshold_10pct": 30.3,
  "vi_minus_1": {
    "mapBased": {
      "rank": 106,
      "score": 0.351598
    },
    "tokenBased": {
      "rank": 204,
      "score": 0.175926
    },
    "treeBased": {
      "rank": 199,
      "score": 0.278689
    }
  },
  "vi": {
    "mapBased": {
      "rank": 112,
      "score": 0.351598
    },
    "tokenBased": {
      "rank": 255,
      "score": 0.175926
    },
    "treeBased": {
      "rank": 247,
      "score": 0.278689
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
      "vi1_rank": 204,
      "vi_rank": 255,
      "delta": -51,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 199,
      "vi_rank": 247,
      "delta": -48,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `R_candidates/Vi-1_v0.18.1/scipy.special._spherical_bessel.spherical_kn.py`
- **new**: `R_candidates/Vi_v0.19.0/scipy.special._spherical_bessel.spherical_kn.py`
- **+0 / -0**

```diff
```

```json
{
  "old_file": "R_candidates/Vi-1_v0.18.1/scipy.special._spherical_bessel.spherical_kn.py",
  "new_file": "R_candidates/Vi_v0.19.0/scipy.special._spherical_bessel.spherical_kn.py",
  "lines_added": 0,
  "lines_removed": 0
}
```
