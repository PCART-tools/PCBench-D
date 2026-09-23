# 一、突变情况分析

- **Total**: 18
- **替代API**: `django.contrib.staticfiles.storage.ManifestStaticFilesStorage`
- **10% 阈值**: 1.8

## Vi-1 (2.1.8-3.1)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 1 | 0.8500 |
| tokenBased | 1 | 0.6190 |

## Vi (2.2-3.1)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 5 | 0.2500 |
| tokenBased | 6 | 0.2889 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 1 | 5 | -4 | true |
| tokenBased | 1 | 6 | -5 | true |

```json
{
  "total": 18,
  "replacement_api": "django.contrib.staticfiles.storage.ManifestStaticFilesStorage",
  "threshold_10pct": 1.8,
  "vi_minus_1": {
    "mapBased": {
      "rank": 1,
      "score": 0.85
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.619048
    }
  },
  "vi": {
    "mapBased": {
      "rank": 5,
      "score": 0.25
    },
    "tokenBased": {
      "rank": 6,
      "score": 0.288889
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 1,
      "vi_rank": 5,
      "delta": -4,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 1,
      "vi_rank": 6,
      "delta": -5,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `django.contrib.staticfiles.storage.CachedStaticFilesStorage/Vi-1_2.1.8.py`
- **new**: `django.contrib.staticfiles.storage.CachedStaticFilesStorage/Vi_2.2.py`
- **+7 / -1**

```diff
--- django.contrib.staticfiles.storage.CachedStaticFilesStorage/Vi-1_2.1.8.py
+++ django.contrib.staticfiles.storage.CachedStaticFilesStorage/Vi_2.2.py
@@ -1,3 +1,9 @@
 class CachedStaticFilesStorage(CachedFilesMixin, StaticFilesStorage):
     
-    pass
+    def __init__(self, *args, **kwargs):
+        warnings.warn(
+            'CachedStaticFilesStorage is deprecated in favor of '
+            'ManifestStaticFilesStorage.',
+            RemovedInDjango31Warning, stacklevel=2,
+        )
+        super().__init__(*args, **kwargs)
```

```json
{
  "old_file": "django.contrib.staticfiles.storage.CachedStaticFilesStorage/Vi-1_2.1.8.py",
  "new_file": "django.contrib.staticfiles.storage.CachedStaticFilesStorage/Vi_2.2.py",
  "lines_added": 7,
  "lines_removed": 1
}
```
