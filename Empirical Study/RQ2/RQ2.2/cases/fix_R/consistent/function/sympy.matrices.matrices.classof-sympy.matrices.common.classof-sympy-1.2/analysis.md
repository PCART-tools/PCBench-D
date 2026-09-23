# 一、突变情况分析

- **Total**: 865
- **替代API**: `sympy.matrices.common.classof`
- **10% 阈值**: 86.5

## Vi-1 (sympy-1.2-sympy-1.12)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 1 | 0.6621 |
| tokenBased | 1 | 0.7308 |
| treeBased | 1 | 0.7616 |

## Vi (sympy-1.3-sympy-1.12)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 217 | 0.2346 |
| tokenBased | 166 | 0.1667 |
| treeBased | 396 | 0.2762 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 1 | 217 | -216 | true |
| tokenBased | 1 | 166 | -165 | true |
| treeBased | 1 | 396 | -395 | true |

```json
{
  "total": 865,
  "replacement_api": "sympy.matrices.common.classof",
  "threshold_10pct": 86.5,
  "vi_minus_1": {
    "mapBased": {
      "rank": 1,
      "score": 0.662059
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.730769
    },
    "treeBased": {
      "rank": 1,
      "score": 0.761589
    }
  },
  "vi": {
    "mapBased": {
      "rank": 217,
      "score": 0.234649
    },
    "tokenBased": {
      "rank": 166,
      "score": 0.166667
    },
    "treeBased": {
      "rank": 396,
      "score": 0.27619
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 1,
      "vi_rank": 217,
      "delta": -216,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 1,
      "vi_rank": 166,
      "delta": -165,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 1,
      "vi_rank": 396,
      "delta": -395,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `sympy.matrices.matrices.classof/Vi-1_sympy-1.2.py`
- **new**: `sympy.matrices.matrices.classof/Vi_sympy-1.3.py`
- **+6 / -17**

```diff
--- sympy.matrices.matrices.classof/Vi-1_sympy-1.2.py
+++ sympy.matrices.matrices.classof/Vi_sympy-1.3.py
@@ -1,18 +1,7 @@
+@deprecated(
+    issue=15109,
+    useinstead="from sympy.matrices.common import classof",
+    deprecated_since_version="1.3")
 def classof(A, B):
-    
-    try:
-        if A._class_priority > B._class_priority:
-            return A.__class__
-        else:
-            return B.__class__
-    except AttributeError:
-        pass
-    try:
-        import numpy
-        if isinstance(A, numpy.ndarray):
-            return B.__class__
-        if isinstance(B, numpy.ndarray):
-            return A.__class__
-    except (AttributeError, ImportError):
-        pass
-    raise TypeError("Incompatible classes %s, %s" % (A.__class__, B.__class__))
+    from sympy.matrices.common import classof as classof_
+    return classof_(A, B)
```

```json
{
  "old_file": "sympy.matrices.matrices.classof/Vi-1_sympy-1.2.py",
  "new_file": "sympy.matrices.matrices.classof/Vi_sympy-1.3.py",
  "lines_added": 6,
  "lines_removed": 17
}
```
