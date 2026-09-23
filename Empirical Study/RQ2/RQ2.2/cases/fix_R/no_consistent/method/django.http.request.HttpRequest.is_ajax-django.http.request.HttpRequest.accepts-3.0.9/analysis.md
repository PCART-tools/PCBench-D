# 一、突变情况分析

- **Total**: 137
- **替代API**: `django.http.request.HttpRequest.accepts`
- **10% 阈值**: 13.7

## Vi-1 (3.0.9-4.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 32 | 0.8371 |
| tokenBased | 27 | 0.2759 |
| treeBased | 35 | 0.6176 |

## Vi (3.1-4.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 34 | 0.7513 |
| tokenBased | 7 | 0.3333 |
| treeBased | 46 | 0.5000 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 32 | 34 | -2 | false |
| tokenBased | 27 | 7 | +20 | true |
| treeBased | 35 | 46 | -11 | false |

```json
{
  "total": 137,
  "replacement_api": "django.http.request.HttpRequest.accepts",
  "threshold_10pct": 13.7,
  "vi_minus_1": {
    "mapBased": {
      "rank": 32,
      "score": 0.837143
    },
    "tokenBased": {
      "rank": 27,
      "score": 0.275862
    },
    "treeBased": {
      "rank": 35,
      "score": 0.617647
    }
  },
  "vi": {
    "mapBased": {
      "rank": 34,
      "score": 0.751282
    },
    "tokenBased": {
      "rank": 7,
      "score": 0.333333
    },
    "treeBased": {
      "rank": 46,
      "score": 0.5
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 32,
      "vi_rank": 34,
      "delta": -2,
      "exceeds_10pct": false
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 27,
      "vi_rank": 7,
      "delta": 20,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 35,
      "vi_rank": 46,
      "delta": -11,
      "exceeds_10pct": false
    }
  ]
}
```

# 二、old → new Diff

- **old**: `django.http.request.HttpRequest.is_ajax/Vi-1_3.0.9.py`
- **new**: `django.http.request.HttpRequest.is_ajax/Vi_3.1.py`
- **+6 / -0**

```diff
--- django.http.request.HttpRequest.is_ajax/Vi-1_3.0.9.py
+++ django.http.request.HttpRequest.is_ajax/Vi_3.1.py
@@ -1,2 +1,8 @@
     def is_ajax(self):
+        warnings.warn(
+            'request.is_ajax() is deprecated. See Django 3.1 release notes '
+            'for more details about this deprecation.',
+            RemovedInDjango40Warning,
+            stacklevel=2,
+        )
         return self.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
```

```json
{
  "old_file": "django.http.request.HttpRequest.is_ajax/Vi-1_3.0.9.py",
  "new_file": "django.http.request.HttpRequest.is_ajax/Vi_3.1.py",
  "lines_added": 6,
  "lines_removed": 0
}
```
