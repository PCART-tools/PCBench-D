# 一、突变情况分析

- **Total**: 4803
- **替代API**: `matplotlib.collections.QuadMesh.get_paths`
- **10% 阈值**: 480.3

## Vi-1 (v3.4.3-v3.7.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 2095 | 0.3996 |
| tokenBased | 4141 | 0.0619 |
| treeBased | 3281 | 0.2281 |

## Vi (v3.5.0-v3.7.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 1446 | 0.5365 |
| tokenBased | 2605 | 0.1351 |
| treeBased | 1538 | 0.5000 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 2095 | 1446 | +649 | true |
| tokenBased | 4141 | 2605 | +1536 | true |
| treeBased | 3281 | 1538 | +1743 | true |

```json
{
  "total": 4803,
  "replacement_api": "matplotlib.collections.QuadMesh.get_paths",
  "threshold_10pct": 480.3,
  "vi_minus_1": {
    "mapBased": {
      "rank": 2095,
      "score": 0.399617
    },
    "tokenBased": {
      "rank": 4141,
      "score": 0.061856
    },
    "treeBased": {
      "rank": 3281,
      "score": 0.22807
    }
  },
  "vi": {
    "mapBased": {
      "rank": 1446,
      "score": 0.536458
    },
    "tokenBased": {
      "rank": 2605,
      "score": 0.135135
    },
    "treeBased": {
      "rank": 1538,
      "score": 0.5
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 2095,
      "vi_rank": 1446,
      "delta": 649,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 4141,
      "vi_rank": 2605,
      "delta": 1536,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 3281,
      "vi_rank": 1538,
      "delta": 1743,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `matplotlib.collections.QuadMesh.convert_mesh_to_paths/Vi-1_v3.4.3.py`
- **new**: `matplotlib.collections.QuadMesh.convert_mesh_to_paths/Vi_v3.5.0.py`
- **+2 / -14**

```diff
--- matplotlib.collections.QuadMesh.convert_mesh_to_paths/Vi-1_v3.4.3.py
+++ matplotlib.collections.QuadMesh.convert_mesh_to_paths/Vi_v3.5.0.py
@@ -1,16 +1,4 @@
     @staticmethod
+    @_api.deprecated("3.5", alternative="QuadMesh(coordinates).get_paths()")
     def convert_mesh_to_paths(meshWidth, meshHeight, coordinates):
-        
-        if isinstance(coordinates, np.ma.MaskedArray):
-            c = coordinates.data
-        else:
-            c = coordinates
-        points = np.concatenate((
-                    c[:-1, :-1],
-                    c[:-1, 1:],
-                    c[1:, 1:],
-                    c[1:, :-1],
-                    c[:-1, :-1]
-                ), axis=2)
-        points = points.reshape((meshWidth * meshHeight, 5, 2))
-        return [mpath.Path(x) for x in points]
+        return QuadMesh._convert_mesh_to_paths(coordinates)
```

```json
{
  "old_file": "matplotlib.collections.QuadMesh.convert_mesh_to_paths/Vi-1_v3.4.3.py",
  "new_file": "matplotlib.collections.QuadMesh.convert_mesh_to_paths/Vi_v3.5.0.py",
  "lines_added": 2,
  "lines_removed": 14
}
```
