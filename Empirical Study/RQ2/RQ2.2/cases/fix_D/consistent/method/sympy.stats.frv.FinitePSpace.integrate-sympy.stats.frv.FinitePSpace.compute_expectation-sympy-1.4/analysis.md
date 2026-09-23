# 一、突变情况分析

- **Total**: 441
- **替代API**: `sympy.stats.frv.FinitePSpace.compute_expectation`
- **10% 阈值**: 44.1

## Vi-1 (sympy-1.2-sympy-1.4)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 1 | 0.9613 |
| tokenBased | 1 | 0.8214 |
| treeBased | 1 | 0.9604 |

## Vi (sympy-1.2-sympy-1.5)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 84 | 0.6289 |
| tokenBased | 43 | 0.4220 |
| treeBased | 236 | 0.4398 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 1 | 84 | -83 | true |
| tokenBased | 1 | 43 | -42 | false |
| treeBased | 1 | 236 | -235 | true |

```json
{
  "total": 441,
  "replacement_api": "sympy.stats.frv.FinitePSpace.compute_expectation",
  "threshold_10pct": 44.1,
  "vi_minus_1": {
    "mapBased": {
      "rank": 1,
      "score": 0.961276
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.821429
    },
    "treeBased": {
      "rank": 1,
      "score": 0.960396
    }
  },
  "vi": {
    "mapBased": {
      "rank": 84,
      "score": 0.628856
    },
    "tokenBased": {
      "rank": 43,
      "score": 0.422018
    },
    "treeBased": {
      "rank": 236,
      "score": 0.439759
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 1,
      "vi_rank": 84,
      "delta": -83,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 1,
      "vi_rank": 43,
      "delta": -42,
      "exceeds_10pct": false
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 1,
      "vi_rank": 236,
      "delta": -235,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `R_candidates/Vi-1_sympy-1.4/sympy.stats.frv.FinitePSpace.compute_expectation.py`
- **new**: `R_candidates/Vi_sympy-1.5/sympy.stats.frv.FinitePSpace.compute_expectation.py`
- **+10 / -3**

```diff
--- R_candidates/Vi-1_sympy-1.4/sympy.stats.frv.FinitePSpace.compute_expectation.py
+++ R_candidates/Vi_sympy-1.5/sympy.stats.frv.FinitePSpace.compute_expectation.py
@@ -1,5 +1,12 @@
     def compute_expectation(self, expr, rvs=None, **kwargs):
         rvs = rvs or self.values
-        expr = expr.xreplace(dict((rs, rs.symbol) for rs in rvs))
-        return sum([expr.xreplace(dict(elem)) * self.prob_of(elem)
-                for elem in self.domain])
+        expr = rv_subs(expr, rvs)
+        probs = [self.prob_of(elem) for elem in self.domain]
+        if isinstance(expr, (Logic, Relational)):
+            parse_domain = [tuple(elem)[0][1] for elem in self.domain]
+            bools = [expr.xreplace(dict(elem)) for elem in self.domain]
+        else:
+            parse_domain = [expr.xreplace(dict(elem)) for elem in self.domain]
+            bools = [True for elem in self.domain]
+        return sum([Piecewise((prob * elem, blv), (S.Zero, True))
+                for prob, elem, blv in zip(probs, parse_domain, bools)])
```

```json
{
  "old_file": "R_candidates/Vi-1_sympy-1.4/sympy.stats.frv.FinitePSpace.compute_expectation.py",
  "new_file": "R_candidates/Vi_sympy-1.5/sympy.stats.frv.FinitePSpace.compute_expectation.py",
  "lines_added": 10,
  "lines_removed": 3
}
```
