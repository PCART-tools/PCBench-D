# 一、突变情况分析

- **Total**: 64
- **替代API**: `django.db.backends.postgresql.introspection.DatabaseIntrospection.get_constraints`
- **10% 阈值**: 6.4

## Vi-1 (1.10.7-2.1)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 12 | 0.5230 |
| tokenBased | 11 | 0.3234 |
| treeBased | 18 | 0.3968 |

## Vi (1.11-2.1)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 5 | 0.5563 |
| tokenBased | 8 | 0.3491 |
| treeBased | 15 | 0.3962 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 12 | 5 | +7 | true |
| tokenBased | 11 | 8 | +3 | false |
| treeBased | 18 | 15 | +3 | false |

```json
{
  "total": 64,
  "replacement_api": "django.db.backends.postgresql.introspection.DatabaseIntrospection.get_constraints",
  "threshold_10pct": 6.4,
  "vi_minus_1": {
    "mapBased": {
      "rank": 12,
      "score": 0.523006
    },
    "tokenBased": {
      "rank": 11,
      "score": 0.323353
    },
    "treeBased": {
      "rank": 18,
      "score": 0.396825
    }
  },
  "vi": {
    "mapBased": {
      "rank": 5,
      "score": 0.556287
    },
    "tokenBased": {
      "rank": 8,
      "score": 0.349112
    },
    "treeBased": {
      "rank": 15,
      "score": 0.396154
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 12,
      "vi_rank": 5,
      "delta": 7,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 11,
      "vi_rank": 8,
      "delta": 3,
      "exceeds_10pct": false
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 18,
      "vi_rank": 15,
      "delta": 3,
      "exceeds_10pct": false
    }
  ]
}
```

# 二、old → new Diff

- **old**: `django.db.backends.postgresql.introspection.DatabaseIntrospection.get_indexes/Vi-1_1.10.7.py`
- **new**: `django.db.backends.postgresql.introspection.DatabaseIntrospection.get_indexes/Vi_1.11.py`
- **+4 / -0**

```diff
--- django.db.backends.postgresql.introspection.DatabaseIntrospection.get_indexes/Vi-1_1.10.7.py
+++ django.db.backends.postgresql.introspection.DatabaseIntrospection.get_indexes/Vi_1.11.py
@@ -1,4 +1,8 @@
     def get_indexes(self, cursor, table_name):
+        warnings.warn(
+            "get_indexes() is deprecated in favor of get_constraints().",
+            RemovedInDjango21Warning, stacklevel=2
+        )
 
 
         cursor.execute(self._get_indexes_query, [table_name])
```

```json
{
  "old_file": "django.db.backends.postgresql.introspection.DatabaseIntrospection.get_indexes/Vi-1_1.10.7.py",
  "new_file": "django.db.backends.postgresql.introspection.DatabaseIntrospection.get_indexes/Vi_1.11.py",
  "lines_added": 4,
  "lines_removed": 0
}
```
