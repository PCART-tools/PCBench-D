# 一、突变情况分析

- **Total**: 147
- **替代API**: `django.db.backends.oracle.introspection.DatabaseIntrospection.get_constraints`
- **10% 阈值**: 14.7

## Vi-1 (1.10.7-2.1)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 32 | 0.5528 |
| tokenBased | 43 | 0.2903 |
| treeBased | 85 | 0.3810 |

## Vi (1.11-2.1)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 11 | 0.5902 |
| tokenBased | 32 | 0.3185 |
| treeBased | 51 | 0.4128 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 32 | 11 | +21 | true |
| tokenBased | 43 | 32 | +11 | false |
| treeBased | 85 | 51 | +34 | true |

```json
{
  "total": 147,
  "replacement_api": "django.db.backends.oracle.introspection.DatabaseIntrospection.get_constraints",
  "threshold_10pct": 14.7,
  "vi_minus_1": {
    "mapBased": {
      "rank": 32,
      "score": 0.552762
    },
    "tokenBased": {
      "rank": 43,
      "score": 0.290323
    },
    "treeBased": {
      "rank": 85,
      "score": 0.380952
    }
  },
  "vi": {
    "mapBased": {
      "rank": 11,
      "score": 0.59022
    },
    "tokenBased": {
      "rank": 32,
      "score": 0.318471
    },
    "treeBased": {
      "rank": 51,
      "score": 0.412844
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 32,
      "vi_rank": 11,
      "delta": 21,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 43,
      "vi_rank": 32,
      "delta": 11,
      "exceeds_10pct": false
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 85,
      "vi_rank": 51,
      "delta": 34,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `django.db.backends.oracle.introspection.DatabaseIntrospection.get_indexes/Vi-1_1.10.7.py`
- **new**: `django.db.backends.oracle.introspection.DatabaseIntrospection.get_indexes/Vi_1.11.py`
- **+4 / -0**

```diff
--- django.db.backends.oracle.introspection.DatabaseIntrospection.get_indexes/Vi-1_1.10.7.py
+++ django.db.backends.oracle.introspection.DatabaseIntrospection.get_indexes/Vi_1.11.py
@@ -1,4 +1,8 @@
     def get_indexes(self, cursor, table_name):
+        warnings.warn(
+            "get_indexes() is deprecated in favor of get_constraints().",
+            RemovedInDjango21Warning, stacklevel=2
+        )
         sql = """
     SELECT LOWER(uic1.column_name) AS column_name,
            CASE user_constraints.constraint_type
```

```json
{
  "old_file": "django.db.backends.oracle.introspection.DatabaseIntrospection.get_indexes/Vi-1_1.10.7.py",
  "new_file": "django.db.backends.oracle.introspection.DatabaseIntrospection.get_indexes/Vi_1.11.py",
  "lines_added": 4,
  "lines_removed": 0
}
```
