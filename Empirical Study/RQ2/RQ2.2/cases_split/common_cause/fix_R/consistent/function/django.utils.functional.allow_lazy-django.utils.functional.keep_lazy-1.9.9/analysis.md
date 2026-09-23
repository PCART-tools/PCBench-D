# 一、突变情况分析

- **Total**: 286
- **替代API**: `django.utils.functional.keep_lazy`
- **10% 阈值**: 28.6

## Vi-1 (1.9.9-2.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 62 | 0.6159 |
| tokenBased | 1 | 0.7536 |
| treeBased | 1 | 0.8444 |

## Vi (1.10-2.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 153 | 0.4851 |
| tokenBased | 129 | 0.2500 |
| treeBased | 235 | 0.2812 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 62 | 153 | -91 | true |
| tokenBased | 1 | 129 | -128 | true |
| treeBased | 1 | 235 | -234 | true |

```json
{
  "total": 286,
  "replacement_api": "django.utils.functional.keep_lazy",
  "threshold_10pct": 28.6,
  "vi_minus_1": {
    "mapBased": {
      "rank": 62,
      "score": 0.615854
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.753623
    },
    "treeBased": {
      "rank": 1,
      "score": 0.844444
    }
  },
  "vi": {
    "mapBased": {
      "rank": 153,
      "score": 0.48513
    },
    "tokenBased": {
      "rank": 129,
      "score": 0.25
    },
    "treeBased": {
      "rank": 235,
      "score": 0.28125
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 62,
      "vi_rank": 153,
      "delta": -91,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 1,
      "vi_rank": 129,
      "delta": -128,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 1,
      "vi_rank": 235,
      "delta": -234,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `django.utils.functional.allow_lazy/Vi-1_1.9.9.py`
- **new**: `django.utils.functional.allow_lazy/Vi_1.10.py`
- **+5 / -12**

```diff
--- django.utils.functional.allow_lazy/Vi-1_1.9.9.py
+++ django.utils.functional.allow_lazy/Vi_1.10.py
@@ -1,13 +1,6 @@
 def allow_lazy(func, *resultclasses):
-    
-    lazy_func = lazy(func, *resultclasses)
-
-    @wraps(func)
-    def wrapper(*args, **kwargs):
-        for arg in list(args) + list(kwargs.values()):
-            if isinstance(arg, Promise):
-                break
-        else:
-            return func(*args, **kwargs)
-        return lazy_func(*args, **kwargs)
-    return wrapper
+    warnings.warn(
+        "django.utils.functional.allow_lazy() is deprecated in favor of "
+        "django.utils.functional.keep_lazy()",
+        RemovedInDjango20Warning, 2)
+    return keep_lazy(*resultclasses)(func)
```

```json
{
  "old_file": "django.utils.functional.allow_lazy/Vi-1_1.9.9.py",
  "new_file": "django.utils.functional.allow_lazy/Vi_1.10.py",
  "lines_added": 5,
  "lines_removed": 12
}
```
