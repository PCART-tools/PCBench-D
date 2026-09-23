# 一、突变情况分析

- **Total**: 61
- **替代API**: `django.db.models.fields.related_descriptors.ManyToManyDescriptor`
- **10% 阈值**: 6.1

## Vi-1 (1.7.5-1.9)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 10 | 0.2993 |
| tokenBased | 6 | 0.3869 |

## Vi (1.8-1.9)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 9 | 0.2993 |
| tokenBased | 14 | 0.3403 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 10 | 9 | +1 | false |
| tokenBased | 6 | 14 | -8 | true |

```json
{
  "total": 61,
  "replacement_api": "django.db.models.fields.related_descriptors.ManyToManyDescriptor",
  "threshold_10pct": 6.1,
  "vi_minus_1": {
    "mapBased": {
      "rank": 10,
      "score": 0.299294
    },
    "tokenBased": {
      "rank": 6,
      "score": 0.386905
    }
  },
  "vi": {
    "mapBased": {
      "rank": 9,
      "score": 0.299294
    },
    "tokenBased": {
      "rank": 14,
      "score": 0.340314
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 10,
      "vi_rank": 9,
      "delta": 1,
      "exceeds_10pct": false
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 6,
      "vi_rank": 14,
      "delta": -8,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `django.db.models.fields.related.ManyRelatedObjectsDescriptor/Vi-1_1.7.5.py`
- **new**: `django.db.models.fields.related.ManyRelatedObjectsDescriptor/Vi_1.8.py`
- **+14 / -5**

```diff
--- django.db.models.fields.related.ManyRelatedObjectsDescriptor/Vi-1_1.7.5.py
+++ django.db.models.fields.related.ManyRelatedObjectsDescriptor/Vi_1.8.py
@@ -13,7 +13,7 @@
 
 
         return create_many_related_manager(
-            self.related.model._default_manager.__class__,
+            self.related.related_model._default_manager.__class__,
             self.related.field.rel
         )
 
@@ -21,7 +21,7 @@
         if instance is None:
             return self
 
-        rel_model = self.related.model
+        rel_model = self.related.related_model
 
         manager = self.related_manager_cls(
             model=rel_model,
@@ -40,8 +40,17 @@
     def __set__(self, instance, value):
         if not self.related.field.rel.through._meta.auto_created:
             opts = self.related.field.rel.through._meta
-            raise AttributeError("Cannot set values on a ManyToManyField which specifies an intermediary model. Use %s.%s's Manager instead." % (opts.app_label, opts.object_name))
+            raise AttributeError(
+                "Cannot set values on a ManyToManyField which specifies an "
+                "intermediary model. Use %s.%s's Manager instead." % (opts.app_label, opts.object_name)
+            )
+
+
+
+        value = tuple(value)
 
         manager = self.__get__(instance)
-        manager.clear()
-        manager.add(*value)
+        db = router.db_for_write(manager.through, instance=manager.instance)
+        with transaction.atomic(using=db, savepoint=False):
+            manager.clear()
+            manager.add(*value)
```

```json
{
  "old_file": "django.db.models.fields.related.ManyRelatedObjectsDescriptor/Vi-1_1.7.5.py",
  "new_file": "django.db.models.fields.related.ManyRelatedObjectsDescriptor/Vi_1.8.py",
  "lines_added": 14,
  "lines_removed": 5
}
```
