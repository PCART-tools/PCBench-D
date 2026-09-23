# 一、突变情况分析

- **Total**: 413
- **替代API**: `django.db.models.fields.files.FileField.generate_filename`
- **10% 阈值**: 41.3

## Vi-1 (1.9.9-2.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 289 | 0.4135 |
| tokenBased | 29 | 0.3818 |
| treeBased | 294 | 0.4091 |

## Vi (1.10-2.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 303 | 0.4349 |
| tokenBased | 14 | 0.4068 |
| treeBased | 251 | 0.4324 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 289 | 303 | -14 | false |
| tokenBased | 29 | 14 | +15 | false |
| treeBased | 294 | 251 | +43 | true |

```json
{
  "total": 413,
  "replacement_api": "django.db.models.fields.files.FileField.generate_filename",
  "threshold_10pct": 41.3,
  "vi_minus_1": {
    "mapBased": {
      "rank": 289,
      "score": 0.413483
    },
    "tokenBased": {
      "rank": 29,
      "score": 0.381818
    },
    "treeBased": {
      "rank": 294,
      "score": 0.409091
    }
  },
  "vi": {
    "mapBased": {
      "rank": 303,
      "score": 0.434946
    },
    "tokenBased": {
      "rank": 14,
      "score": 0.40678
    },
    "treeBased": {
      "rank": 251,
      "score": 0.432432
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 289,
      "vi_rank": 303,
      "delta": -14,
      "exceeds_10pct": false
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 29,
      "vi_rank": 14,
      "delta": 15,
      "exceeds_10pct": false
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 294,
      "vi_rank": 251,
      "delta": 43,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `django.db.models.fields.files.FileField.get_filename/Vi-1_1.9.9.py`
- **new**: `django.db.models.fields.files.FileField.get_filename/Vi_1.10.py`
- **+5 / -0**

```diff
--- django.db.models.fields.files.FileField.get_filename/Vi-1_1.9.9.py
+++ django.db.models.fields.files.FileField.get_filename/Vi_1.10.py
@@ -1,2 +1,7 @@
     def get_filename(self, filename):
+        warnings.warn(
+            'FileField now delegates file name and folder processing to the '
+            'storage. get_filename() will be removed in Django 2.0.',
+            RemovedInDjango20Warning, stacklevel=2
+        )
         return os.path.normpath(self.storage.get_valid_name(os.path.basename(filename)))
```

```json
{
  "old_file": "django.db.models.fields.files.FileField.get_filename/Vi-1_1.9.9.py",
  "new_file": "django.db.models.fields.files.FileField.get_filename/Vi_1.10.py",
  "lines_added": 5,
  "lines_removed": 0
}
```
