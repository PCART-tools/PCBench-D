# 一、突变情况分析

- **Total**: 325
- **替代API**: `sympy.geometry.line.Line.equals`
- **10% 阈值**: 32.5

## Vi-1 (sympy-0.7.6.1-sympy-1.10)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 1 | 1.0000 |
| tokenBased | 1 | 0.8065 |
| treeBased | 1 | 0.9821 |

## Vi (sympy-1.0-sympy-1.10)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 101 | 0.7273 |
| tokenBased | 101 | 0.2727 |
| treeBased | 117 | 0.5217 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 1 | 101 | -100 | true |
| tokenBased | 1 | 101 | -100 | true |
| treeBased | 1 | 117 | -116 | true |

```json
{
  "total": 325,
  "replacement_api": "sympy.geometry.line.Line.equals",
  "threshold_10pct": 32.5,
  "vi_minus_1": {
    "mapBased": {
      "rank": 1,
      "score": 1.0
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.806452
    },
    "treeBased": {
      "rank": 1,
      "score": 0.982143
    }
  },
  "vi": {
    "mapBased": {
      "rank": 101,
      "score": 0.727273
    },
    "tokenBased": {
      "rank": 101,
      "score": 0.272727
    },
    "treeBased": {
      "rank": 117,
      "score": 0.521739
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 1,
      "vi_rank": 101,
      "delta": -100,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 1,
      "vi_rank": 101,
      "delta": -100,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 1,
      "vi_rank": 117,
      "delta": -116,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `sympy.geometry.line.Line.equal/Vi-1_sympy-0.7.6.1.py`
- **new**: `sympy.geometry.line.Line.equal/Vi_sympy-1.0.py`
- **+2 / -4**

```diff
--- sympy.geometry.line.Line.equal/Vi-1_sympy-0.7.6.1.py
+++ sympy.geometry.line.Line.equal/Vi_sympy-1.0.py
@@ -1,5 +1,3 @@
+    @deprecated(useinstead="equals", deprecated_since_version="1.0")
     def equal(self, other):
-        
-        if not isinstance(other, Line):
-            return False
-        return Point.is_collinear(self.p1, other.p1, self.p2, other.p2)
+        return self.equals(other)
```

```json
{
  "old_file": "sympy.geometry.line.Line.equal/Vi-1_sympy-0.7.6.1.py",
  "new_file": "sympy.geometry.line.Line.equal/Vi_sympy-1.0.py",
  "lines_added": 2,
  "lines_removed": 4
}
```
