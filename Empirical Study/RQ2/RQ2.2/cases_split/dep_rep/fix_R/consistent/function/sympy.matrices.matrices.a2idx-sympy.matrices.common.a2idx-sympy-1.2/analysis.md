# 一、突变情况分析

- **Total**: 865
- **替代API**: `sympy.matrices.common.a2idx`
- **10% 阈值**: 86.5

## Vi-1 (sympy-1.2-sympy-1.12)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 2 | 0.5812 |
| tokenBased | 1 | 0.7595 |
| treeBased | 1 | 0.8533 |

## Vi (sympy-1.3-sympy-1.12)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 139 | 0.2995 |
| tokenBased | 116 | 0.1842 |
| treeBased | 265 | 0.3398 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 2 | 139 | -137 | true |
| tokenBased | 1 | 116 | -115 | true |
| treeBased | 1 | 265 | -264 | true |

```json
{
  "total": 865,
  "replacement_api": "sympy.matrices.common.a2idx",
  "threshold_10pct": 86.5,
  "vi_minus_1": {
    "mapBased": {
      "rank": 2,
      "score": 0.581169
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.759494
    },
    "treeBased": {
      "rank": 1,
      "score": 0.853333
    }
  },
  "vi": {
    "mapBased": {
      "rank": 139,
      "score": 0.299465
    },
    "tokenBased": {
      "rank": 116,
      "score": 0.184211
    },
    "treeBased": {
      "rank": 265,
      "score": 0.339806
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 2,
      "vi_rank": 139,
      "delta": -137,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 1,
      "vi_rank": 116,
      "delta": -115,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 1,
      "vi_rank": 265,
      "delta": -264,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `sympy.matrices.matrices.a2idx/Vi-1_sympy-1.2.py`
- **new**: `sympy.matrices.matrices.a2idx/Vi_sympy-1.3.py`
- **+6 / -12**

```diff
--- sympy.matrices.matrices.a2idx/Vi-1_sympy-1.2.py
+++ sympy.matrices.matrices.a2idx/Vi_sympy-1.3.py
@@ -1,13 +1,7 @@
+@deprecated(
+    issue=15109,
+    deprecated_since_version="1.3",
+    useinstead="from sympy.matrices.common import a2idx")
 def a2idx(j, n=None):
-    
-    if type(j) is not int:
-        try:
-            j = j.__index__()
-        except AttributeError:
-            raise IndexError("Invalid index a[%r]" % (j,))
-    if n is not None:
-        if j < 0:
-            j += n
-        if not (j >= 0 and j < n):
-            raise IndexError("Index out of range: a[%s]" % j)
-    return int(j)
+    from sympy.matrices.common import a2idx as a2idx_
+    return a2idx_(j, n)
```

```json
{
  "old_file": "sympy.matrices.matrices.a2idx/Vi-1_sympy-1.2.py",
  "new_file": "sympy.matrices.matrices.a2idx/Vi_sympy-1.3.py",
  "lines_added": 6,
  "lines_removed": 12
}
```
