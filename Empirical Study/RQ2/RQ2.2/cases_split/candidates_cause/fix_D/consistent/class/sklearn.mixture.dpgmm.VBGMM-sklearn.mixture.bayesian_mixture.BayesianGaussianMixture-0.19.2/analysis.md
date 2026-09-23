# 一、突变情况分析

- **Total**: 24
- **替代API**: `sklearn.mixture.bayesian_mixture.BayesianGaussianMixture`
- **10% 阈值**: 2.4

## Vi-1 (0.17.1-0.19.2)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 6 | 0.1399 |
| tokenBased | 7 | 0.2661 |

## Vi (0.17.1-0.20.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 2 | 0.1399 |
| tokenBased | 4 | 0.2661 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 6 | 2 | +4 | true |
| tokenBased | 7 | 4 | +3 | true |

```json
{
  "total": 24,
  "replacement_api": "sklearn.mixture.bayesian_mixture.BayesianGaussianMixture",
  "threshold_10pct": 2.4,
  "vi_minus_1": {
    "mapBased": {
      "rank": 6,
      "score": 0.139924
    },
    "tokenBased": {
      "rank": 7,
      "score": 0.266055
    }
  },
  "vi": {
    "mapBased": {
      "rank": 2,
      "score": 0.139924
    },
    "tokenBased": {
      "rank": 4,
      "score": 0.266055
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 6,
      "vi_rank": 2,
      "delta": 4,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 7,
      "vi_rank": 4,
      "delta": 3,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `R_candidates/Vi-1_0.19.2/sklearn.mixture.bayesian_mixture.BayesianGaussianMixture.py`
- **new**: `R_candidates/Vi_0.20.0/sklearn.mixture.bayesian_mixture.BayesianGaussianMixture.py`
- **+0 / -0**

```diff
```

```json
{
  "old_file": "R_candidates/Vi-1_0.19.2/sklearn.mixture.bayesian_mixture.BayesianGaussianMixture.py",
  "new_file": "R_candidates/Vi_0.20.0/sklearn.mixture.bayesian_mixture.BayesianGaussianMixture.py",
  "lines_added": 0,
  "lines_removed": 0
}
```
