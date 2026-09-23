# 一、突变情况分析

- **Total**: 369
- **替代API**: `polars.string_cache.enable_string_cache`
- **10% 阈值**: 36.9

## Vi-1 (py-0.16.18-py-0.19.3)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 1 | 0.9947 |
| tokenBased | 1 | 0.6800 |
| treeBased | 1 | 0.9167 |

## Vi (py-0.16.18-py-0.19.4)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 141 | 0.4477 |
| tokenBased | 3 | 0.3542 |
| treeBased | 114 | 0.4118 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 1 | 141 | -140 | true |
| tokenBased | 1 | 3 | -2 | false |
| treeBased | 1 | 114 | -113 | true |

```json
{
  "total": 369,
  "replacement_api": "polars.string_cache.enable_string_cache",
  "threshold_10pct": 36.9,
  "vi_minus_1": {
    "mapBased": {
      "rank": 1,
      "score": 0.994665
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.68
    },
    "treeBased": {
      "rank": 1,
      "score": 0.916667
    }
  },
  "vi": {
    "mapBased": {
      "rank": 141,
      "score": 0.447695
    },
    "tokenBased": {
      "rank": 3,
      "score": 0.354167
    },
    "treeBased": {
      "rank": 114,
      "score": 0.411765
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 1,
      "vi_rank": 141,
      "delta": -140,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 1,
      "vi_rank": 3,
      "delta": -2,
      "exceeds_10pct": false
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 1,
      "vi_rank": 114,
      "delta": -113,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `R_candidates/Vi-1_py-0.19.3/polars.string_cache.enable_string_cache.py`
- **new**: `R_candidates/Vi_py-0.19.4/polars.string_cache.enable_string_cache.py`
- **+13 / -2**

```diff
--- R_candidates/Vi-1_py-0.19.3/polars.string_cache.enable_string_cache.py
+++ R_candidates/Vi_py-0.19.4/polars.string_cache.enable_string_cache.py
@@ -1,3 +1,14 @@
-def enable_string_cache(enable: bool) -> None:
+def enable_string_cache(enable: bool | None = None) -> None:
     
-    _enable_string_cache(enable)
+    if enable is not None:
+        issue_deprecation_warning(
+            "`enable_string_cache` no longer accepts an argument."
+            " Call `enable_string_cache()` to enable the string cache"
+            " and `disable_string_cache()` to disable the string cache.",
+            version="0.19.3",
+        )
+        if enable is False:
+            plr.disable_string_cache()
+            return
+
+    plr.enable_string_cache()
```

```json
{
  "old_file": "R_candidates/Vi-1_py-0.19.3/polars.string_cache.enable_string_cache.py",
  "new_file": "R_candidates/Vi_py-0.19.4/polars.string_cache.enable_string_cache.py",
  "lines_added": 13,
  "lines_removed": 2
}
```
