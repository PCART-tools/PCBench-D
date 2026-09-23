# 一、突变情况分析

- **Total**: 90
- **替代API**: `django.contrib.gis.db.models.functions.ForcePolygonCW`
- **10% 阈值**: 9.0

## Vi-1 (2.0.8-3.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 1 | 0.8500 |
| tokenBased | 1 | 0.5714 |

## Vi (2.1-3.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 15 | 0.2500 |
| tokenBased | 24 | 0.2667 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 1 | 15 | -14 | true |
| tokenBased | 1 | 24 | -23 | true |

```json
{
  "total": 90,
  "replacement_api": "django.contrib.gis.db.models.functions.ForcePolygonCW",
  "threshold_10pct": 9.0,
  "vi_minus_1": {
    "mapBased": {
      "rank": 1,
      "score": 0.85
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.571429
    }
  },
  "vi": {
    "mapBased": {
      "rank": 15,
      "score": 0.25
    },
    "tokenBased": {
      "rank": 24,
      "score": 0.266667
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 1,
      "vi_rank": 15,
      "delta": -14,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 1,
      "vi_rank": 24,
      "delta": -23,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `django.contrib.gis.db.models.functions.ForceRHR/Vi-1_2.0.8.py`
- **new**: `django.contrib.gis.db.models.functions.ForceRHR/Vi_2.1.py`
- **+7 / -0**

```diff
--- django.contrib.gis.db.models.functions.ForceRHR/Vi-1_2.0.8.py
+++ django.contrib.gis.db.models.functions.ForceRHR/Vi_2.1.py
@@ -1,2 +1,9 @@
 class ForceRHR(GeomOutputGeoFunc):
     arity = 1
+
+    def __init__(self, *args, **kwargs):
+        warnings.warn(
+            'ForceRHR is deprecated in favor of ForcePolygonCW.',
+            RemovedInDjango30Warning, stacklevel=2,
+        )
+        super().__init__(*args, **kwargs)
```

```json
{
  "old_file": "django.contrib.gis.db.models.functions.ForceRHR/Vi-1_2.0.8.py",
  "new_file": "django.contrib.gis.db.models.functions.ForceRHR/Vi_2.1.py",
  "lines_added": 7,
  "lines_removed": 0
}
```
