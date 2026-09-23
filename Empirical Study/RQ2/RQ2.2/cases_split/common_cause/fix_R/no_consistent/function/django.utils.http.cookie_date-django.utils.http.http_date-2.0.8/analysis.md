# 一、突变情况分析

- **Total**: 276
- **替代API**: `django.utils.http.http_date`
- **10% 阈值**: 27.6

## Vi-1 (2.0.8-3.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 35 | 0.6941 |
| tokenBased | 5 | 0.3611 |
| treeBased | 33 | 0.4889 |

## Vi (2.1-3.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 31 | 0.6401 |
| tokenBased | 52 | 0.3023 |
| treeBased | 128 | 0.4151 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 35 | 31 | +4 | false |
| tokenBased | 5 | 52 | -47 | true |
| treeBased | 33 | 128 | -95 | true |

```json
{
  "total": 276,
  "replacement_api": "django.utils.http.http_date",
  "threshold_10pct": 27.6,
  "vi_minus_1": {
    "mapBased": {
      "rank": 35,
      "score": 0.694093
    },
    "tokenBased": {
      "rank": 5,
      "score": 0.361111
    },
    "treeBased": {
      "rank": 33,
      "score": 0.488889
    }
  },
  "vi": {
    "mapBased": {
      "rank": 31,
      "score": 0.640078
    },
    "tokenBased": {
      "rank": 52,
      "score": 0.302326
    },
    "treeBased": {
      "rank": 128,
      "score": 0.415094
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 35,
      "vi_rank": 31,
      "delta": 4,
      "exceeds_10pct": false
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 5,
      "vi_rank": 52,
      "delta": -47,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 33,
      "vi_rank": 128,
      "delta": -95,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `django.utils.http.cookie_date/Vi-1_2.0.8.py`
- **new**: `django.utils.http.cookie_date/Vi_2.1.py`
- **+5 / -0**

```diff
--- django.utils.http.cookie_date/Vi-1_2.0.8.py
+++ django.utils.http.cookie_date/Vi_2.1.py
@@ -1,4 +1,9 @@
 def cookie_date(epoch_seconds=None):
     
+    warnings.warn(
+        'cookie_date() is deprecated in favor of http_date(), which follows '
+        'the format of the latest RFC.',
+        RemovedInDjango30Warning, stacklevel=2,
+    )
     rfcdate = formatdate(epoch_seconds)
     return '%s-%s-%s GMT' % (rfcdate[:7], rfcdate[8:11], rfcdate[12:25])
```

```json
{
  "old_file": "django.utils.http.cookie_date/Vi-1_2.0.8.py",
  "new_file": "django.utils.http.cookie_date/Vi_2.1.py",
  "lines_added": 5,
  "lines_removed": 0
}
```
