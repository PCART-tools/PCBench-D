# 一、突变情况分析

- **Total**: 239
- **替代API**: `django.contrib.gis.geos.point.Point.tuple`
- **10% 阈值**: 23.9

## Vi-1 (1.9.9-2.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 140 | 0.5745 |
| tokenBased | 134 | 0.2273 |
| treeBased | 58 | 0.6800 |

## Vi (1.10-2.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 179 | 0.3874 |
| tokenBased | 180 | 0.2222 |
| treeBased | 141 | 0.5484 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 140 | 179 | -39 | true |
| tokenBased | 134 | 180 | -46 | true |
| treeBased | 58 | 141 | -83 | true |

```json
{
  "total": 239,
  "replacement_api": "django.contrib.gis.geos.point.Point.tuple",
  "threshold_10pct": 23.9,
  "vi_minus_1": {
    "mapBased": {
      "rank": 140,
      "score": 0.574468
    },
    "tokenBased": {
      "rank": 134,
      "score": 0.227273
    },
    "treeBased": {
      "rank": 58,
      "score": 0.68
    }
  },
  "vi": {
    "mapBased": {
      "rank": 179,
      "score": 0.387435
    },
    "tokenBased": {
      "rank": 180,
      "score": 0.222222
    },
    "treeBased": {
      "rank": 141,
      "score": 0.548387
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 140,
      "vi_rank": 179,
      "delta": -39,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 134,
      "vi_rank": 180,
      "delta": -46,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 58,
      "vi_rank": 141,
      "delta": -83,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `django.contrib.gis.geos.point.Point.get_coords/Vi-1_1.9.9.py`
- **new**: `django.contrib.gis.geos.point.Point.get_coords/Vi_1.10.py`
- **+5 / -2**

```diff
--- django.contrib.gis.geos.point.Point.get_coords/Vi-1_1.9.9.py
+++ django.contrib.gis.geos.point.Point.get_coords/Vi_1.10.py
@@ -1,3 +1,6 @@
     def get_coords(self):
-        
-        return self._cs.tuple
+        warnings.warn(
+            "`get_coords()` is deprecated, use the `tuple` property instead.",
+            RemovedInDjango20Warning, 2
+        )
+        return self.tuple
```

```json
{
  "old_file": "django.contrib.gis.geos.point.Point.get_coords/Vi-1_1.9.9.py",
  "new_file": "django.contrib.gis.geos.point.Point.get_coords/Vi_1.10.py",
  "lines_added": 5,
  "lines_removed": 2
}
```
