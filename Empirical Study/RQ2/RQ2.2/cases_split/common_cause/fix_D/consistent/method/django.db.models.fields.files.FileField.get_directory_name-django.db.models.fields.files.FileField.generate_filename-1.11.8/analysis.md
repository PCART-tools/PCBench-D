# 一、突变情况分析

- **Total**: 408
- **替代API**: `django.db.models.fields.files.FileField.generate_filename`
- **10% 阈值**: 40.8

## Vi-1 (1.9.9-1.11.8)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 293 | 0.3571 |
| tokenBased | 7 | 0.3692 |
| treeBased | 47 | 0.5417 |

## Vi (1.9.9-2.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 294 | 0.3571 |
| tokenBased | 21 | 0.3607 |
| treeBased | 148 | 0.4853 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 293 | 294 | -1 | false |
| tokenBased | 7 | 21 | -14 | false |
| treeBased | 47 | 148 | -101 | true |

```json
{
  "total": 408,
  "replacement_api": "django.db.models.fields.files.FileField.generate_filename",
  "threshold_10pct": 40.8,
  "vi_minus_1": {
    "mapBased": {
      "rank": 293,
      "score": 0.357143
    },
    "tokenBased": {
      "rank": 7,
      "score": 0.369231
    },
    "treeBased": {
      "rank": 47,
      "score": 0.541667
    }
  },
  "vi": {
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
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 293,
      "vi_rank": 294,
      "delta": -1,
      "exceeds_10pct": false
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 7,
      "vi_rank": 21,
      "delta": -14,
      "exceeds_10pct": false
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 47,
      "vi_rank": 148,
      "delta": -101,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `R_candidates/Vi-1_1.11.8/django.db.models.fields.files.FileField.generate_filename.py`
- **new**: `R_candidates/Vi_2.0/django.db.models.fields.files.FileField.generate_filename.py`
- **+1 / -1**

```diff
--- R_candidates/Vi-1_1.11.8/django.db.models.fields.files.FileField.generate_filename.py
+++ R_candidates/Vi_2.0/django.db.models.fields.files.FileField.generate_filename.py
@@ -3,6 +3,6 @@
         if callable(self.upload_to):
             filename = self.upload_to(instance, filename)
         else:
-            dirname = force_text(datetime.datetime.now().strftime(force_str(self.upload_to)))
+            dirname = datetime.datetime.now().strftime(self.upload_to)
             filename = posixpath.join(dirname, filename)
         return self.storage.generate_filename(filename)
```

```json
{
  "old_file": "R_candidates/Vi-1_1.11.8/django.db.models.fields.files.FileField.generate_filename.py",
  "new_file": "R_candidates/Vi_2.0/django.db.models.fields.files.FileField.generate_filename.py",
  "lines_added": 1,
  "lines_removed": 1
}
```
