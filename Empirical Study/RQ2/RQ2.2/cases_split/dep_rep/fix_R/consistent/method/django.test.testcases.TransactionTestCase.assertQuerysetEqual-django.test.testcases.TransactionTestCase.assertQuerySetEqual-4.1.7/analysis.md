# 一、突变情况分析

- **Total**: 326
- **替代API**: `django.test.testcases.TransactionTestCase.assertQuerySetEqual`
- **10% 阈值**: 32.6

## Vi-1 (4.1.7-5.1)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 1 | 1.0000 |
| tokenBased | 1 | 0.8723 |
| treeBased | 1 | 0.9940 |

## Vi (4.2-5.1)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 217 | 0.3666 |
| tokenBased | 242 | 0.1717 |
| treeBased | 282 | 0.3148 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 1 | 217 | -216 | true |
| tokenBased | 1 | 242 | -241 | true |
| treeBased | 1 | 282 | -281 | true |

```json
{
  "total": 326,
  "replacement_api": "django.test.testcases.TransactionTestCase.assertQuerySetEqual",
  "threshold_10pct": 32.6,
  "vi_minus_1": {
    "mapBased": {
      "rank": 1,
      "score": 1.0
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.87234
    },
    "treeBased": {
      "rank": 1,
      "score": 0.993976
    }
  },
  "vi": {
    "mapBased": {
      "rank": 217,
      "score": 0.366628
    },
    "tokenBased": {
      "rank": 242,
      "score": 0.171717
    },
    "treeBased": {
      "rank": 282,
      "score": 0.314815
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 1,
      "vi_rank": 217,
      "delta": -216,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 1,
      "vi_rank": 242,
      "delta": -241,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 1,
      "vi_rank": 282,
      "delta": -281,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `django.test.testcases.TransactionTestCase.assertQuerysetEqual/Vi-1_4.1.7.py`
- **new**: `django.test.testcases.TransactionTestCase.assertQuerysetEqual/Vi_4.2.py`
- **+7 / -15**

```diff
--- django.test.testcases.TransactionTestCase.assertQuerysetEqual/Vi-1_4.1.7.py
+++ django.test.testcases.TransactionTestCase.assertQuerysetEqual/Vi_4.2.py
@@ -1,15 +1,7 @@
-    def assertQuerysetEqual(self, qs, values, transform=None, ordered=True, msg=None):
-        values = list(values)
-        items = qs
-        if transform is not None:
-            items = map(transform, items)
-        if not ordered:
-            return self.assertDictEqual(Counter(items), Counter(values), msg=msg)
-
-
-        if len(values) > 1 and hasattr(qs, "ordered") and not qs.ordered:
-            raise ValueError(
-                "Trying to compare non-ordered queryset against more than one "
-                "ordered value."
-            )
-        return self.assertEqual(list(items), values, msg=msg)
+    def assertQuerysetEqual(self, *args, **kw):
+        warnings.warn(
+            "assertQuerysetEqual() is deprecated in favor of assertQuerySetEqual().",
+            category=RemovedInDjango51Warning,
+            stacklevel=2,
+        )
+        return self.assertQuerySetEqual(*args, **kw)
```

```json
{
  "old_file": "django.test.testcases.TransactionTestCase.assertQuerysetEqual/Vi-1_4.1.7.py",
  "new_file": "django.test.testcases.TransactionTestCase.assertQuerysetEqual/Vi_4.2.py",
  "lines_added": 7,
  "lines_removed": 15
}
```
