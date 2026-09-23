# 一、突变情况分析

- **Total**: 326
- **替代API**: `django.test.testcases.SimpleTestCase.assertFormSetError`
- **10% 阈值**: 32.6

## Vi-1 (4.1.7-5.1)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 1 | 0.7012 |
| tokenBased | 1 | 0.8163 |
| treeBased | 1 | 0.9353 |

## Vi (4.2-5.1)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 315 | 0.1769 |
| tokenBased | 301 | 0.1159 |
| treeBased | 312 | 0.2118 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 1 | 315 | -314 | true |
| tokenBased | 1 | 301 | -300 | true |
| treeBased | 1 | 312 | -311 | true |

```json
{
  "total": 326,
  "replacement_api": "django.test.testcases.SimpleTestCase.assertFormSetError",
  "threshold_10pct": 32.6,
  "vi_minus_1": {
    "mapBased": {
      "rank": 1,
      "score": 0.701244
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.816327
    },
    "treeBased": {
      "rank": 1,
      "score": 0.935275
    }
  },
  "vi": {
    "mapBased": {
      "rank": 315,
      "score": 0.176876
    },
    "tokenBased": {
      "rank": 301,
      "score": 0.115942
    },
    "treeBased": {
      "rank": 312,
      "score": 0.211765
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 1,
      "vi_rank": 315,
      "delta": -314,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 1,
      "vi_rank": 301,
      "delta": -300,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 1,
      "vi_rank": 312,
      "delta": -311,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `django.test.testcases.SimpleTestCase.assertFormsetError/Vi-1_4.1.7.py`
- **new**: `django.test.testcases.SimpleTestCase.assertFormsetError/Vi_4.2.py`
- **+7 / -41**

```diff
--- django.test.testcases.SimpleTestCase.assertFormsetError/Vi-1_4.1.7.py
+++ django.test.testcases.SimpleTestCase.assertFormsetError/Vi_4.2.py
@@ -1,41 +1,7 @@
-    @_AssertFormErrorDeprecationHelper.patch_signature
-    def assertFormsetError(self, formset, form_index, field, errors, msg_prefix=""):
-        
-        if errors is None:
-            warnings.warn(
-                "Passing errors=None to assertFormsetError() is deprecated, "
-                "use errors=[] instead.",
-                RemovedInDjango50Warning,
-                stacklevel=2,
-            )
-            errors = []
-
-        if form_index is None and field is not None:
-            raise ValueError("You must use field=None with form_index=None.")
-
-        if msg_prefix:
-            msg_prefix += ": "
-        errors = to_list(errors)
-
-        if not formset.is_bound:
-            self.fail(
-                f"{msg_prefix}The formset {formset!r} is not bound, it will never have "
-                f"any errors."
-            )
-        if form_index is not None and form_index >= formset.total_form_count():
-            form_count = formset.total_form_count()
-            form_or_forms = "forms" if form_count > 1 else "form"
-            self.fail(
-                f"{msg_prefix}The formset {formset!r} only has {form_count} "
-                f"{form_or_forms}."
-            )
-        if form_index is not None:
-            form_repr = f"form {form_index} of formset {formset!r}"
-            self._assert_form_error(
-                formset.forms[form_index], field, errors, msg_prefix, form_repr
-            )
-        else:
-            failure_message = f"The non-form errors of formset {formset!r} don't match."
-            self.assertEqual(
-                formset.non_form_errors(), errors, msg_prefix + failure_message
-            )
+    def assertFormsetError(self, *args, **kw):
+        warnings.warn(
+            "assertFormsetError() is deprecated in favor of assertFormSetError().",
+            category=RemovedInDjango51Warning,
+            stacklevel=2,
+        )
+        return self.assertFormSetError(*args, **kw)
```

```json
{
  "old_file": "django.test.testcases.SimpleTestCase.assertFormsetError/Vi-1_4.1.7.py",
  "new_file": "django.test.testcases.SimpleTestCase.assertFormsetError/Vi_4.2.py",
  "lines_added": 7,
  "lines_removed": 41
}
```
