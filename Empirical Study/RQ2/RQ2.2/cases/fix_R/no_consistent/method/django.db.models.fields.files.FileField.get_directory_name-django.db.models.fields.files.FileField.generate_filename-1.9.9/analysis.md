# 一、突变情况分析

- **Total**: 413
- **替代API**: `django.db.models.fields.files.FileField.generate_filename`
- **10% 阈值**: 41.3

## Vi-1 (1.9.9-2.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 294 | 0.3571 |
| tokenBased | 21 | 0.3607 |
| treeBased | 148 | 0.4853 |

## Vi (1.10-2.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 311 | 0.3824 |
| tokenBased | 7 | 0.3846 |
| treeBased | 80 | 0.4868 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 294 | 311 | -17 | false |
| tokenBased | 21 | 7 | +14 | false |
| treeBased | 148 | 80 | +68 | true |

```json
{
  "total": 413,
  "replacement_api": "django.db.models.fields.files.FileField.generate_filename",
  "threshold_10pct": 41.3,
  "vi_minus_1": {
    "mapBased": {
      "rank": 294,
      "score": 0.357143
    },
    "tokenBased": {
      "rank": 21,
      "score": 0.360656
    },
    "treeBased": {
      "rank": 148,
      "score": 0.485294
    }
  },
  "vi": {
    "mapBased": {
      "rank": 311,
      "score": 0.382386
    },
    "tokenBased": {
      "rank": 7,
      "score": 0.384615
    },
    "treeBased": {
      "rank": 80,
      "score": 0.486842
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 294,
      "vi_rank": 311,
      "delta": -17,
      "exceeds_10pct": false
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 21,
      "vi_rank": 7,
      "delta": 14,
      "exceeds_10pct": false
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 148,
      "vi_rank": 80,
      "delta": 68,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `django.db.models.fields.files.FileField.get_directory_name/Vi-1_1.9.9.py`
- **new**: `django.db.models.fields.files.FileField.get_directory_name/Vi_1.10.py`
- **+5 / -0**

```diff
--- django.db.models.fields.files.FileField.get_directory_name/Vi-1_1.9.9.py
+++ django.db.models.fields.files.FileField.get_directory_name/Vi_1.10.py
@@ -1,2 +1,7 @@
     def get_directory_name(self):
+        warnings.warn(
+            'FileField now delegates file name and folder processing to the '
+            'storage. get_directory_name() will be removed in Django 2.0.',
+            RemovedInDjango20Warning, stacklevel=2
+        )
         return os.path.normpath(force_text(datetime.datetime.now().strftime(force_str(self.upload_to))))
```

```json
{
  "old_file": "django.db.models.fields.files.FileField.get_directory_name/Vi-1_1.9.9.py",
  "new_file": "django.db.models.fields.files.FileField.get_directory_name/Vi_1.10.py",
  "lines_added": 5,
  "lines_removed": 0
}
```
