# 一、突变情况分析

- **Total**: 150
- **替代API**: `django.db.backends.oracle.introspection.DatabaseIntrospection.get_constraints`
- **10% 阈值**: 15.0

## Vi-1 (1.10.7-2.1.8)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 32 | 0.5528 |
| tokenBased | 44 | 0.2903 |
| treeBased | 86 | 0.3810 |

## Vi (1.10.7-2.2)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 73 | 0.4390 |
| tokenBased | 66 | 0.2601 |
| treeBased | 102 | 0.3509 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 32 | 73 | -41 | true |
| tokenBased | 44 | 66 | -22 | true |
| treeBased | 86 | 102 | -16 | true |

```json
{
  "total": 150,
  "replacement_api": "django.db.backends.oracle.introspection.DatabaseIntrospection.get_constraints",
  "threshold_10pct": 15.0,
  "vi_minus_1": {
    "mapBased": {
      "rank": 32,
      "score": 0.552762
    },
    "tokenBased": {
      "rank": 44,
      "score": 0.290323
    },
    "treeBased": {
      "rank": 86,
      "score": 0.380952
    }
  },
  "vi": {
    "mapBased": {
      "rank": 73,
      "score": 0.438976
    },
    "tokenBased": {
      "rank": 66,
      "score": 0.260116
    },
    "treeBased": {
      "rank": 102,
      "score": 0.350877
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 32,
      "vi_rank": 73,
      "delta": -41,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 44,
      "vi_rank": 66,
      "delta": -22,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 86,
      "vi_rank": 102,
      "delta": -16,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `R_candidates/Vi-1_2.1.8/django.db.backends.oracle.introspection.DatabaseIntrospection.get_constraints.py`
- **new**: `R_candidates/Vi_2.2/django.db.backends.oracle.introspection.DatabaseIntrospection.get_constraints.py`
- **+3 / -0**

```diff
--- R_candidates/Vi-1_2.1.8/django.db.backends.oracle.introspection.DatabaseIntrospection.get_constraints.py
+++ R_candidates/Vi_2.2/django.db.backends.oracle.introspection.DatabaseIntrospection.get_constraints.py
@@ -28,6 +28,7 @@
             GROUP BY user_constraints.constraint_name, user_constraints.constraint_type
         """, [table_name])
         for constraint, columns, pk, unique, check in cursor.fetchall():
+            constraint = self.identifier_converter(constraint)
             constraints[constraint] = {
                 'columns': columns.split(','),
                 'primary_key': pk,
@@ -55,6 +56,7 @@
             GROUP BY cons.constraint_name, rcols.table_name, rcols.column_name
         """, [table_name])
         for constraint, columns, other_table, other_column in cursor.fetchall():
+            constraint = self.identifier_converter(constraint)
             constraints[constraint] = {
                 'primary_key': False,
                 'unique': False,
@@ -82,6 +84,7 @@
             GROUP BY ind.index_name, ind.index_type
         """, [table_name])
         for constraint, type_, columns, orders in cursor.fetchall():
+            constraint = self.identifier_converter(constraint)
             constraints[constraint] = {
                 'primary_key': False,
                 'unique': False,
```

```json
{
  "old_file": "R_candidates/Vi-1_2.1.8/django.db.backends.oracle.introspection.DatabaseIntrospection.get_constraints.py",
  "new_file": "R_candidates/Vi_2.2/django.db.backends.oracle.introspection.DatabaseIntrospection.get_constraints.py",
  "lines_added": 3,
  "lines_removed": 0
}
```
