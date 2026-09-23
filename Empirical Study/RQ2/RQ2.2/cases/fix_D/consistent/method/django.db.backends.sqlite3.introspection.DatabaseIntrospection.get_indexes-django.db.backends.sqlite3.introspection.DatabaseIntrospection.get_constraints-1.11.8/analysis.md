# 一、突变情况分析

- **Total**: 78
- **替代API**: `django.db.backends.sqlite3.introspection.DatabaseIntrospection.get_constraints`
- **10% 阈值**: 7.8

## Vi-1 (1.10.7-1.11.8)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 3 | 0.4932 |
| tokenBased | 4 | 0.4931 |
| treeBased | 3 | 0.4765 |

## Vi (1.10.7-2.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 6 | 0.4451 |
| tokenBased | 12 | 0.4113 |
| treeBased | 7 | 0.4383 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 3 | 6 | -3 | false |
| tokenBased | 4 | 12 | -8 | true |
| treeBased | 3 | 7 | -4 | false |

```json
{
  "total": 78,
  "replacement_api": "django.db.backends.sqlite3.introspection.DatabaseIntrospection.get_constraints",
  "threshold_10pct": 7.8,
  "vi_minus_1": {
    "mapBased": {
      "rank": 3,
      "score": 0.493159
    },
    "tokenBased": {
      "rank": 4,
      "score": 0.493088
    },
    "treeBased": {
      "rank": 3,
      "score": 0.476471
    }
  },
  "vi": {
    "mapBased": {
      "rank": 6,
      "score": 0.445131
    },
    "tokenBased": {
      "rank": 12,
      "score": 0.411321
    },
    "treeBased": {
      "rank": 7,
      "score": 0.438287
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 3,
      "vi_rank": 6,
      "delta": -3,
      "exceeds_10pct": false
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 4,
      "vi_rank": 12,
      "delta": -8,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 3,
      "vi_rank": 7,
      "delta": -4,
      "exceeds_10pct": false
    }
  ]
}
```

# 二、old → new Diff

- **old**: `R_candidates/Vi-1_1.11.8/django.db.backends.sqlite3.introspection.DatabaseIntrospection.get_constraints.py`
- **new**: `R_candidates/Vi_2.0/django.db.backends.sqlite3.introspection.DatabaseIntrospection.get_constraints.py`
- **+13 / -0**

```diff
--- R_candidates/Vi-1_1.11.8/django.db.backends.sqlite3.introspection.DatabaseIntrospection.get_constraints.py
+++ R_candidates/Vi_2.0/django.db.backends.sqlite3.introspection.DatabaseIntrospection.get_constraints.py
@@ -49,4 +49,17 @@
                 "check": False,
                 "index": False,
             }
+
+        cursor.execute('PRAGMA foreign_key_list(%s)' % self.connection.ops.quote_name(table_name))
+        for row in cursor.fetchall():
+
+            id_, seq, table, from_, to = row[:5]
+            constraints['fk_%d' % id_] = {
+                'columns': [from_],
+                'primary_key': False,
+                'unique': False,
+                'foreign_key': (table, to),
+                'check': False,
+                'index': False,
+            }
         return constraints
```

```json
{
  "old_file": "R_candidates/Vi-1_1.11.8/django.db.backends.sqlite3.introspection.DatabaseIntrospection.get_constraints.py",
  "new_file": "R_candidates/Vi_2.0/django.db.backends.sqlite3.introspection.DatabaseIntrospection.get_constraints.py",
  "lines_added": 13,
  "lines_removed": 0
}
```
