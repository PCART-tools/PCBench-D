# 一、突变情况分析

- **Total**: 5001
- **替代API**: `matplotlib.contour.ContourLabeler.add_label`
- **10% 阈值**: 500.1

## Vi-1 (v3.8.4-v3.10.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 343 | 0.5853 |
| tokenBased | 30 | 0.4364 |
| treeBased | 127 | 0.5089 |

## Vi (v3.9.0-v3.10.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 1189 | 0.4157 |
| tokenBased | 1259 | 0.2321 |
| treeBased | 4009 | 0.3072 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 343 | 1189 | -846 | true |
| tokenBased | 30 | 1259 | -1229 | true |
| treeBased | 127 | 4009 | -3882 | true |

```json
{
  "total": 5001,
  "replacement_api": "matplotlib.contour.ContourLabeler.add_label",
  "threshold_10pct": 500.1,
  "vi_minus_1": {
    "mapBased": {
      "rank": 343,
      "score": 0.58533
    },
    "tokenBased": {
      "rank": 30,
      "score": 0.436364
    },
    "treeBased": {
      "rank": 127,
      "score": 0.508876
    }
  },
  "vi": {
    "mapBased": {
      "rank": 1189,
      "score": 0.415708
    },
    "tokenBased": {
      "rank": 1259,
      "score": 0.232143
    },
    "treeBased": {
      "rank": 4009,
      "score": 0.30719
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 343,
      "vi_rank": 1189,
      "delta": -846,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 30,
      "vi_rank": 1259,
      "delta": -1229,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 127,
      "vi_rank": 4009,
      "delta": -3882,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `matplotlib.contour.ContourLabeler.add_label_clabeltext/Vi-1_v3.8.4.py`
- **new**: `matplotlib.contour.ContourLabeler.add_label_clabeltext/Vi_v3.9.0.py`
- **+3 / -6**

```diff
--- matplotlib.contour.ContourLabeler.add_label_clabeltext/Vi-1_v3.8.4.py
+++ matplotlib.contour.ContourLabeler.add_label_clabeltext/Vi_v3.9.0.py
@@ -1,8 +1,5 @@
+    @_api.deprecated("3.8", alternative="add_label")
     def add_label_clabeltext(self, x, y, rotation, lev, cvalue):
         
-        self.add_label(x, y, rotation, lev, cvalue)
-
-        t = self.labelTexts[-1]
-        data_rotation, = self.axes.transData.inverted().transform_angles(
-            [rotation], [[x, y]])
-        t.set(rotation=data_rotation, transform_rotates_text=True)
+        with cbook._setattr_cm(self, _use_clabeltext=True):
+            self.add_label(x, y, rotation, lev, cvalue)
```

```json
{
  "old_file": "matplotlib.contour.ContourLabeler.add_label_clabeltext/Vi-1_v3.8.4.py",
  "new_file": "matplotlib.contour.ContourLabeler.add_label_clabeltext/Vi_v3.9.0.py",
  "lines_added": 3,
  "lines_removed": 6
}
```
