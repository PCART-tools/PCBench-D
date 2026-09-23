# 一、突变情况分析

- **Total**: 83
- **替代API**: `django.db.backends.postgresql.operations.DatabaseOperations.on_conflict_suffix_sql`
- **10% 阈值**: 8.3

## Vi-1 (4.0.7-4.1.7)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 64 | 0.3622 |
| tokenBased | 37 | 0.2297 |
| treeBased | 66 | 0.3171 |

## Vi (4.0.7-4.2)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 70 | 0.3622 |
| tokenBased | 46 | 0.2297 |
| treeBased | 75 | 0.3171 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 64 | 70 | -6 | false |
| tokenBased | 37 | 46 | -9 | true |
| treeBased | 66 | 75 | -9 | true |

```json
{
  "total": 83,
  "replacement_api": "django.db.backends.postgresql.operations.DatabaseOperations.on_conflict_suffix_sql",
  "threshold_10pct": 8.3,
  "vi_minus_1": {
    "mapBased": {
      "rank": 64,
      "score": 0.362155
    },
    "tokenBased": {
      "rank": 37,
      "score": 0.22973
    },
    "treeBased": {
      "rank": 66,
      "score": 0.317073
    }
  },
  "vi": {
    "mapBased": {
      "rank": 70,
      "score": 0.362155
    },
    "tokenBased": {
      "rank": 46,
      "score": 0.22973
    },
    "treeBased": {
      "rank": 75,
      "score": 0.317073
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 64,
      "vi_rank": 70,
      "delta": -6,
      "exceeds_10pct": false
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 37,
      "vi_rank": 46,
      "delta": -9,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 66,
      "vi_rank": 75,
      "delta": -9,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `R_candidates/Vi-1_4.1.7/django.db.backends.postgresql.operations.DatabaseOperations.on_conflict_suffix_sql.py`
- **new**: `R_candidates/Vi_4.2/django.db.backends.postgresql.operations.DatabaseOperations.on_conflict_suffix_sql.py`
- **+0 / -0**

```diff
```

```json
{
  "old_file": "R_candidates/Vi-1_4.1.7/django.db.backends.postgresql.operations.DatabaseOperations.on_conflict_suffix_sql.py",
  "new_file": "R_candidates/Vi_4.2/django.db.backends.postgresql.operations.DatabaseOperations.on_conflict_suffix_sql.py",
  "lines_added": 0,
  "lines_removed": 0
}
```
