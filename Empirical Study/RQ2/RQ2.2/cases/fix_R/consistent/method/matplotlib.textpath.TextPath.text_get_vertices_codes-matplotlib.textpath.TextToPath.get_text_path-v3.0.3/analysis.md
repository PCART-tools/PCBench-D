# 一、突变情况分析

- **Total**: 4801
- **替代API**: `matplotlib.textpath.TextToPath.get_text_path`
- **10% 阈值**: 480.1

## Vi-1 (v3.0.3-v3.3.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 1625 | 0.4028 |
| tokenBased | 607 | 0.3433 |
| treeBased | 1720 | 0.4286 |

## Vi (v3.1.0-v3.3.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 3024 | 0.3359 |
| tokenBased | 1703 | 0.2574 |
| treeBased | 3412 | 0.3333 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 1625 | 3024 | -1399 | true |
| tokenBased | 607 | 1703 | -1096 | true |
| treeBased | 1720 | 3412 | -1692 | true |

```json
{
  "total": 4801,
  "replacement_api": "matplotlib.textpath.TextToPath.get_text_path",
  "threshold_10pct": 480.1,
  "vi_minus_1": {
    "mapBased": {
      "rank": 1625,
      "score": 0.402837
    },
    "tokenBased": {
      "rank": 607,
      "score": 0.343284
    },
    "treeBased": {
      "rank": 1720,
      "score": 0.428571
    }
  },
  "vi": {
    "mapBased": {
      "rank": 3024,
      "score": 0.33588
    },
    "tokenBased": {
      "rank": 1703,
      "score": 0.257353
    },
    "treeBased": {
      "rank": 3412,
      "score": 0.333333
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 1625,
      "vi_rank": 3024,
      "delta": -1399,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 607,
      "vi_rank": 1703,
      "delta": -1096,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 1720,
      "vi_rank": 3412,
      "delta": -1692,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `matplotlib.textpath.TextPath.text_get_vertices_codes/Vi-1_v3.0.3.py`
- **new**: `matplotlib.textpath.TextPath.text_get_vertices_codes/Vi_v3.1.0.py`
- **+3 / -5**

```diff
--- matplotlib.textpath.TextPath.text_get_vertices_codes/Vi-1_v3.0.3.py
+++ matplotlib.textpath.TextPath.text_get_vertices_codes/Vi_v3.1.0.py
@@ -1,11 +1,9 @@
+    @cbook.deprecated("3.1", alternative="TextPath")
     def text_get_vertices_codes(self, prop, s, usetex):
         
 
         if usetex:
-            verts, codes = text_to_path.get_text_path(prop, s, usetex=True)
+            return text_to_path.get_text_path(prop, s, usetex=True)
         else:
             clean_line, ismath = self.is_math_text(s)
-            verts, codes = text_to_path.get_text_path(prop, clean_line,
-                                                      ismath=ismath)
-
-        return verts, codes
+            return text_to_path.get_text_path(prop, clean_line, ismath=ismath)
```

```json
{
  "old_file": "matplotlib.textpath.TextPath.text_get_vertices_codes/Vi-1_v3.0.3.py",
  "new_file": "matplotlib.textpath.TextPath.text_get_vertices_codes/Vi_v3.1.0.py",
  "lines_added": 3,
  "lines_removed": 5
}
```
