# 一、突变情况分析

- **Total**: 140
- **替代API**: `django.db.backends.oracle.introspection.DatabaseIntrospection.get_constraints`
- **10% 阈值**: 14.0

## Vi-1 (1.10.7-1.11.8)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 101 | 0.4040 |
| tokenBased | 69 | 0.2460 |
| treeBased | 118 | 0.3083 |

## Vi (1.10.7-2.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 32 | 0.5528 |
| tokenBased | 42 | 0.2903 |
| treeBased | 81 | 0.3810 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 101 | 32 | +69 | true |
| tokenBased | 69 | 42 | +27 | true |
| treeBased | 118 | 81 | +37 | true |

```json
{
  "total": 140,
  "replacement_api": "django.db.backends.oracle.introspection.DatabaseIntrospection.get_constraints",
  "threshold_10pct": 14.0,
  "vi_minus_1": {
    "mapBased": {
      "rank": 101,
      "score": 0.403986
    },
    "tokenBased": {
      "rank": 69,
      "score": 0.245989
    },
    "treeBased": {
      "rank": 118,
      "score": 0.3083
    }
  },
  "vi": {
    "mapBased": {
      "rank": 32,
      "score": 0.552762
    },
    "tokenBased": {
      "rank": 42,
      "score": 0.290323
    },
    "treeBased": {
      "rank": 81,
      "score": 0.380952
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 101,
      "vi_rank": 32,
      "delta": 69,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 69,
      "vi_rank": 42,
      "delta": 27,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 118,
      "vi_rank": 81,
      "delta": 37,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `R_candidates/Vi-1_1.11.8/django.db.backends.oracle.introspection.DatabaseIntrospection.get_constraints.py`
- **new**: `R_candidates/Vi_2.0/django.db.backends.oracle.introspection.DatabaseIntrospection.get_constraints.py`
- **+42 / -63**

```diff
--- R_candidates/Vi-1_1.11.8/django.db.backends.oracle.introspection.DatabaseIntrospection.get_constraints.py
+++ R_candidates/Vi_2.0/django.db.backends.oracle.introspection.DatabaseIntrospection.get_constraints.py
@@ -5,29 +5,19 @@
         cursor.execute("""
             SELECT
                 user_constraints.constraint_name,
-                LOWER(cols.column_name) AS column_name,
+                LISTAGG(LOWER(cols.column_name), ',') WITHIN GROUP (ORDER BY cols.position),
                 CASE user_constraints.constraint_type
                     WHEN 'P' THEN 1
                     ELSE 0
                 END AS is_primary_key,
                 CASE
-                    WHEN EXISTS (
-                        SELECT 1
-                        FROM user_indexes
-                        WHERE user_indexes.index_name = user_constraints.index_name
-                        AND user_indexes.uniqueness = 'UNIQUE'
-                    )
-                    THEN 1
+                    WHEN user_constraints.constraint_type IN ('P', 'U') THEN 1
                     ELSE 0
                 END AS is_unique,
                 CASE user_constraints.constraint_type
                     WHEN 'C' THEN 1
                     ELSE 0
-                END AS is_check_constraint,
-                CASE
-                    WHEN user_constraints.constraint_type IN ('P', 'U') THEN 1
-                    ELSE 0
-                END AS has_index
+                END AS is_check_constraint
             FROM
                 user_constraints
             LEFT OUTER JOIN
@@ -35,57 +25,51 @@
             WHERE
                 user_constraints.constraint_type = ANY('P', 'U', 'C')
                 AND user_constraints.table_name = UPPER(%s)
-            ORDER BY cols.position
+            GROUP BY user_constraints.constraint_name, user_constraints.constraint_type
         """, [table_name])
-        for constraint, column, pk, unique, check, index in cursor.fetchall():
-
-            if constraint not in constraints:
-                constraints[constraint] = {
-                    "columns": [],
-                    "primary_key": pk,
-                    "unique": unique,
-                    "foreign_key": None,
-                    "check": check,
-                    "index": index,
-                }
-
-            constraints[constraint]['columns'].append(column)
+        for constraint, columns, pk, unique, check in cursor.fetchall():
+            constraints[constraint] = {
+                'columns': columns.split(','),
+                'primary_key': pk,
+                'unique': unique,
+                'foreign_key': None,
+                'check': check,
+                'index': unique,
+            }
 
         cursor.execute("""
             SELECT
                 cons.constraint_name,
-                LOWER(cols.column_name) AS column_name,
+                LISTAGG(LOWER(cols.column_name), ',') WITHIN GROUP (ORDER BY cols.position),
                 LOWER(rcols.table_name),
                 LOWER(rcols.column_name)
             FROM
                 user_constraints cons
             INNER JOIN
-                user_cons_columns rcols ON rcols.constraint_name = cons.r_constraint_name
+                user_cons_columns rcols ON rcols.constraint_name = cons.r_constraint_name AND rcols.position = 1
             LEFT OUTER JOIN
                 user_cons_columns cols ON cons.constraint_name = cols.constraint_name
             WHERE
                 cons.constraint_type = 'R' AND
                 cons.table_name = UPPER(%s)
-            ORDER BY cols.position
+            GROUP BY cons.constraint_name, rcols.table_name, rcols.column_name
         """, [table_name])
-        for constraint, column, other_table, other_column in cursor.fetchall():
-
-            if constraint not in constraints:
-                constraints[constraint] = {
-                    "columns": [],
-                    "primary_key": False,
-                    "unique": False,
-                    "foreign_key": (other_table, other_column),
-                    "check": False,
-                    "index": False,
-                }
-
-            constraints[constraint]['columns'].append(column)
+        for constraint, columns, other_table, other_column in cursor.fetchall():
+            constraints[constraint] = {
+                'primary_key': False,
+                'unique': False,
+                'foreign_key': (other_table, other_column),
+                'check': False,
+                'index': False,
+                'columns': columns.split(','),
+            }
 
         cursor.execute("""
             SELECT
-                cols.index_name, LOWER(cols.column_name), cols.descend,
-                LOWER(ind.index_type)
+                ind.index_name,
+                LOWER(ind.index_type),
+                LISTAGG(LOWER(cols.column_name), ',') WITHIN GROUP (ORDER BY cols.column_position),
+                LISTAGG(cols.descend, ',') WITHIN GROUP (ORDER BY cols.column_position)
             FROM
                 user_ind_columns cols, user_indexes ind
             WHERE
@@ -93,24 +77,19 @@
                 NOT EXISTS (
                     SELECT 1
                     FROM user_constraints cons
-                    WHERE cols.index_name = cons.index_name
+                    WHERE ind.index_name = cons.index_name
                 ) AND cols.index_name = ind.index_name
-            ORDER BY cols.column_position
+            GROUP BY ind.index_name, ind.index_type
         """, [table_name])
-        for constraint, column, order, type_ in cursor.fetchall():
-
-            if constraint not in constraints:
-                constraints[constraint] = {
-                    "columns": [],
-                    "orders": [],
-                    "primary_key": False,
-                    "unique": False,
-                    "foreign_key": None,
-                    "check": False,
-                    "index": True,
-                    "type": 'idx' if type_ == 'normal' else type_,
-                }
-
-            constraints[constraint]['columns'].append(column)
-            constraints[constraint]['orders'].append(order)
+        for constraint, type_, columns, orders in cursor.fetchall():
+            constraints[constraint] = {
+                'primary_key': False,
+                'unique': False,
+                'foreign_key': None,
+                'check': False,
+                'index': True,
+                'type': 'idx' if type_ == 'normal' else type_,
+                'columns': columns.split(','),
+                'orders': orders.split(','),
+            }
         return constraints
```

```json
{
  "old_file": "R_candidates/Vi-1_1.11.8/django.db.backends.oracle.introspection.DatabaseIntrospection.get_constraints.py",
  "new_file": "R_candidates/Vi_2.0/django.db.backends.oracle.introspection.DatabaseIntrospection.get_constraints.py",
  "lines_added": 42,
  "lines_removed": 63
}
```
