# 一、突变情况分析

- **Total**: 206
- **替代API**: `django.db.backends.base.operations.BaseDatabaseOperations.check_expression_support`
- **10% 阈值**: 20.6

## Vi-1 (1.8.7-2.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 77 | 0.5745 |
| tokenBased | 1 | 0.5000 |
| treeBased | 70 | 0.7000 |

## Vi (1.9-2.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 93 | 0.5192 |
| tokenBased | 1 | 0.3793 |
| treeBased | 117 | 0.5000 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 77 | 93 | -16 | false |
| tokenBased | 1 | 1 | +0 | false |
| treeBased | 70 | 117 | -47 | true |

```json
{
  "total": 206,
  "replacement_api": "django.db.backends.base.operations.BaseDatabaseOperations.check_expression_support",
  "threshold_10pct": 20.6,
  "vi_minus_1": {
    "mapBased": {
      "rank": 77,
      "score": 0.574468
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.5
    },
    "treeBased": {
      "rank": 70,
      "score": 0.7
    }
  },
  "vi": {
    "mapBased": {
      "rank": 93,
      "score": 0.519231
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.37931
    },
    "treeBased": {
      "rank": 117,
      "score": 0.5
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 77,
      "vi_rank": 93,
      "delta": -16,
      "exceeds_10pct": false
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 1,
      "vi_rank": 1,
      "delta": 0,
      "exceeds_10pct": false
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 70,
      "vi_rank": 117,
      "delta": -47,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `django.db.backends.base.operations.BaseDatabaseOperations.check_aggregate_support/Vi-1_1.8.7.py`
- **new**: `django.db.backends.base.operations.BaseDatabaseOperations.check_aggregate_support/Vi_1.9.py`
- **+4 / -0**

```diff
--- django.db.backends.base.operations.BaseDatabaseOperations.check_aggregate_support/Vi-1_1.8.7.py
+++ django.db.backends.base.operations.BaseDatabaseOperations.check_aggregate_support/Vi_1.9.py
@@ -1,2 +1,6 @@
     def check_aggregate_support(self, aggregate_func):
+        warnings.warn(
+            "check_aggregate_support has been deprecated. Use "
+            "check_expression_support instead.",
+            RemovedInDjango20Warning, stacklevel=2)
         return self.check_expression_support(aggregate_func)
```

```json
{
  "old_file": "django.db.backends.base.operations.BaseDatabaseOperations.check_aggregate_support/Vi-1_1.8.7.py",
  "new_file": "django.db.backends.base.operations.BaseDatabaseOperations.check_aggregate_support/Vi_1.9.py",
  "lines_added": 4,
  "lines_removed": 0
}
```
