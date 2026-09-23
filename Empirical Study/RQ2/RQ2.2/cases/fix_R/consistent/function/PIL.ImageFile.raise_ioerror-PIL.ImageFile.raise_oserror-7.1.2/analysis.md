# 一、突变情况分析

- **Total**: 329
- **替代API**: `PIL.ImageFile.raise_oserror`
- **10% 阈值**: 32.9

## Vi-1 (7.1.2-9.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 1 | 0.9967 |
| tokenBased | 1 | 0.8478 |
| treeBased | 1 | 0.9620 |

## Vi (7.2.0-9.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 241 | 0.2570 |
| tokenBased | 72 | 0.3125 |
| treeBased | 187 | 0.4107 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 1 | 241 | -240 | true |
| tokenBased | 1 | 72 | -71 | true |
| treeBased | 1 | 187 | -186 | true |

```json
{
  "total": 329,
  "replacement_api": "PIL.ImageFile.raise_oserror",
  "threshold_10pct": 32.9,
  "vi_minus_1": {
    "mapBased": {
      "rank": 1,
      "score": 0.996686
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.847826
    },
    "treeBased": {
      "rank": 1,
      "score": 0.962025
    }
  },
  "vi": {
    "mapBased": {
      "rank": 241,
      "score": 0.256964
    },
    "tokenBased": {
      "rank": 72,
      "score": 0.3125
    },
    "treeBased": {
      "rank": 187,
      "score": 0.410714
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 1,
      "vi_rank": 241,
      "delta": -240,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 1,
      "vi_rank": 72,
      "delta": -71,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 1,
      "vi_rank": 187,
      "delta": -186,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `PIL.ImageFile.raise_ioerror/Vi-1_7.1.2.py`
- **new**: `PIL.ImageFile.raise_ioerror/Vi_7.2.0.py`
- **+6 / -7**

```diff
--- PIL.ImageFile.raise_ioerror/Vi-1_7.1.2.py
+++ PIL.ImageFile.raise_ioerror/Vi_7.2.0.py
@@ -1,8 +1,7 @@
 def raise_ioerror(error):
-    try:
-        message = Image.core.getcodecstatus(error)
-    except AttributeError:
-        message = ERRORS.get(error)
-    if not message:
-        message = "decoder error %d" % error
-    raise OSError(message + " when reading image file")
+    warnings.warn(
+        "raise_ioerror is deprecated and will be removed in a future release. "
+        "Use raise_oserror instead.",
+        DeprecationWarning,
+    )
+    return raise_oserror(error)
```

```json
{
  "old_file": "PIL.ImageFile.raise_ioerror/Vi-1_7.1.2.py",
  "new_file": "PIL.ImageFile.raise_ioerror/Vi_7.2.0.py",
  "lines_added": 6,
  "lines_removed": 7
}
```
