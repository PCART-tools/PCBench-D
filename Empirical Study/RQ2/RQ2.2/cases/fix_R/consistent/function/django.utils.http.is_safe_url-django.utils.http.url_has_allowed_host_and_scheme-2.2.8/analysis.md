# 一、突变情况分析

- **Total**: 275
- **替代API**: `django.utils.http.url_has_allowed_host_and_scheme`
- **10% 阈值**: 27.5

## Vi-1 (2.2.8-4.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 1 | 1.0000 |
| tokenBased | 1 | 0.7922 |
| treeBased | 1 | 0.9773 |

## Vi (3.0-4.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 185 | 0.3564 |
| tokenBased | 90 | 0.2692 |
| treeBased | 160 | 0.4111 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 1 | 185 | -184 | true |
| tokenBased | 1 | 90 | -89 | true |
| treeBased | 1 | 160 | -159 | true |

```json
{
  "total": 275,
  "replacement_api": "django.utils.http.url_has_allowed_host_and_scheme",
  "threshold_10pct": 27.5,
  "vi_minus_1": {
    "mapBased": {
      "rank": 1,
      "score": 1.0
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.792208
    },
    "treeBased": {
      "rank": 1,
      "score": 0.977273
    }
  },
  "vi": {
    "mapBased": {
      "rank": 185,
      "score": 0.356431
    },
    "tokenBased": {
      "rank": 90,
      "score": 0.269231
    },
    "treeBased": {
      "rank": 160,
      "score": 0.411111
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 1,
      "vi_rank": 185,
      "delta": -184,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 1,
      "vi_rank": 90,
      "delta": -89,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 1,
      "vi_rank": 160,
      "delta": -159,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `django.utils.http.is_safe_url/Vi-1_2.2.8.py`
- **new**: `django.utils.http.is_safe_url/Vi_3.0.py`
- **+6 / -13**

```diff
--- django.utils.http.is_safe_url/Vi-1_2.2.8.py
+++ django.utils.http.is_safe_url/Vi_3.0.py
@@ -1,14 +1,7 @@
 def is_safe_url(url, allowed_hosts, require_https=False):
-    
-    if url is not None:
-        url = url.strip()
-    if not url:
-        return False
-    if allowed_hosts is None:
-        allowed_hosts = set()
-    elif isinstance(allowed_hosts, str):
-        allowed_hosts = {allowed_hosts}
-
-
-    return (_is_safe_url(url, allowed_hosts, require_https=require_https) and
-            _is_safe_url(url.replace('\\', '/'), allowed_hosts, require_https=require_https))
+    warnings.warn(
+        'django.utils.http.is_safe_url() is deprecated in favor of '
+        'url_has_allowed_host_and_scheme().',
+        RemovedInDjango40Warning, stacklevel=2,
+    )
+    return url_has_allowed_host_and_scheme(url, allowed_hosts, require_https)
```

```json
{
  "old_file": "django.utils.http.is_safe_url/Vi-1_2.2.8.py",
  "new_file": "django.utils.http.is_safe_url/Vi_3.0.py",
  "lines_added": 6,
  "lines_removed": 13
}
```
