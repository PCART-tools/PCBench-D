# 一、突变情况分析

- **Total**: 443
- **替代API**: `polars.expr.expr.Expr.gather_every`
- **10% 阈值**: 44.3

## Vi-1 (py-0.19.13-py-0.20.2)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 1 | 1.0000 |
| tokenBased | 2 | 0.7333 |
| treeBased | 1 | 0.9444 |

## Vi (py-0.19.13-py-0.20.3)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 108 | 0.9035 |
| tokenBased | 5 | 0.5946 |
| treeBased | 95 | 0.8293 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 1 | 108 | -107 | true |
| tokenBased | 2 | 5 | -3 | false |
| treeBased | 1 | 95 | -94 | true |

```json
{
  "total": 443,
  "replacement_api": "polars.expr.expr.Expr.gather_every",
  "threshold_10pct": 44.3,
  "vi_minus_1": {
    "mapBased": {
      "rank": 1,
      "score": 1.0
    },
    "tokenBased": {
      "rank": 2,
      "score": 0.733333
    },
    "treeBased": {
      "rank": 1,
      "score": 0.944444
    }
  },
  "vi": {
    "mapBased": {
      "rank": 108,
      "score": 0.903475
    },
    "tokenBased": {
      "rank": 5,
      "score": 0.594595
    },
    "treeBased": {
      "rank": 95,
      "score": 0.829268
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 1,
      "vi_rank": 108,
      "delta": -107,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 2,
      "vi_rank": 5,
      "delta": -3,
      "exceeds_10pct": false
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 1,
      "vi_rank": 95,
      "delta": -94,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `R_candidates/Vi-1_py-0.20.2/polars.expr.expr.Expr.gather_every.py`
- **new**: `R_candidates/Vi_py-0.20.3/polars.expr.expr.Expr.gather_every.py`
- **+2 / -2**

```diff
--- R_candidates/Vi-1_py-0.20.2/polars.expr.expr.Expr.gather_every.py
+++ R_candidates/Vi_py-0.20.3/polars.expr.expr.Expr.gather_every.py
@@ -1,3 +1,3 @@
-    def gather_every(self, n: int) -> Self:
+    def gather_every(self, n: int, offset: int = 0) -> Self:
         
-        return self._from_pyexpr(self._pyexpr.gather_every(n))
+        return self._from_pyexpr(self._pyexpr.gather_every(n, offset))
```

```json
{
  "old_file": "R_candidates/Vi-1_py-0.20.2/polars.expr.expr.Expr.gather_every.py",
  "new_file": "R_candidates/Vi_py-0.20.3/polars.expr.expr.Expr.gather_every.py",
  "lines_added": 2,
  "lines_removed": 2
}
```
