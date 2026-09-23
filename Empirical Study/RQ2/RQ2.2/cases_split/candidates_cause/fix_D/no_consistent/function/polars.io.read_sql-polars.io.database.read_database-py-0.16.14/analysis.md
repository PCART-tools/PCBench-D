# 一、突变情况分析

- **Total**: 25
- **替代API**: `polars.io.database.read_database`
- **10% 阈值**: 2.5

## Vi-1 (py-0.16.9-py-0.16.14)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 13 | 0.4501 |
| tokenBased | 3 | 0.6620 |
| treeBased | 3 | 0.6343 |

## Vi (py-0.16.9-py-0.16.15)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 23 | 0.4501 |
| tokenBased | 3 | 0.6620 |
| treeBased | 3 | 0.6343 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 13 | 23 | -10 | true |
| tokenBased | 3 | 3 | +0 | false |
| treeBased | 3 | 3 | +0 | false |

```json
{
  "total": 25,
  "replacement_api": "polars.io.database.read_database",
  "threshold_10pct": 2.5,
  "vi_minus_1": {
    "mapBased": {
      "rank": 13,
      "score": 0.450067
    },
    "tokenBased": {
      "rank": 3,
      "score": 0.661972
    },
    "treeBased": {
      "rank": 3,
      "score": 0.634286
    }
  },
  "vi": {
    "mapBased": {
      "rank": 23,
      "score": 0.450067
    },
    "tokenBased": {
      "rank": 3,
      "score": 0.661972
    },
    "treeBased": {
      "rank": 3,
      "score": 0.634286
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 13,
      "vi_rank": 23,
      "delta": -10,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 3,
      "vi_rank": 3,
      "delta": 0,
      "exceeds_10pct": false
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 3,
      "vi_rank": 3,
      "delta": 0,
      "exceeds_10pct": false
    }
  ]
}
```

# 二、old → new Diff

- **old**: `R_candidates/Vi-1_py-0.16.14/polars.io.database.read_database.py`
- **new**: `R_candidates/Vi_py-0.16.15/polars.io.database.read_database.py`
- **+0 / -0**

```diff
```

```json
{
  "old_file": "R_candidates/Vi-1_py-0.16.14/polars.io.database.read_database.py",
  "new_file": "R_candidates/Vi_py-0.16.15/polars.io.database.read_database.py",
  "lines_added": 0,
  "lines_removed": 0
}
```
