# 一、突变情况分析

- **Total**: 457
- **替代API**: `polars.expr.expr.Expr.gather_every`
- **10% 阈值**: 45.7

## Vi-1 (py-0.20.2-py-1.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 76 | 0.9035 |
| tokenBased | 2 | 0.4359 |
| treeBased | 72 | 0.6190 |

## Vi (py-0.20.3-py-1.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 1 | 1.0000 |
| tokenBased | 1 | 0.6154 |
| treeBased | 2 | 0.7660 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 76 | 1 | +75 | true |
| tokenBased | 2 | 1 | +1 | false |
| treeBased | 72 | 2 | +70 | true |

```json
{
  "total": 457,
  "replacement_api": "polars.expr.expr.Expr.gather_every",
  "threshold_10pct": 45.7,
  "vi_minus_1": {
    "mapBased": {
      "rank": 76,
      "score": 0.903475
    },
    "tokenBased": {
      "rank": 2,
      "score": 0.435897
    },
    "treeBased": {
      "rank": 72,
      "score": 0.619048
    }
  },
  "vi": {
    "mapBased": {
      "rank": 1,
      "score": 1.0
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.615385
    },
    "treeBased": {
      "rank": 2,
      "score": 0.765957
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 76,
      "vi_rank": 1,
      "delta": 75,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 2,
      "vi_rank": 1,
      "delta": 1,
      "exceeds_10pct": false
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 72,
      "vi_rank": 2,
      "delta": 70,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `polars.expr.expr.Expr.take_every/Vi-1_py-0.20.2.py`
- **new**: `polars.expr.expr.Expr.take_every/Vi_py-0.20.3.py`
- **+2 / -2**

```diff
--- polars.expr.expr.Expr.take_every/Vi-1_py-0.20.2.py
+++ polars.expr.expr.Expr.take_every/Vi_py-0.20.3.py
@@ -1,4 +1,4 @@
     @deprecate_renamed_function("gather_every", version="0.19.14")
-    def take_every(self, n: int) -> Self:
+    def take_every(self, n: int, offset: int = 0) -> Self:
         
-        return self.gather_every(n)
+        return self.gather_every(n, offset)
```

```json
{
  "old_file": "polars.expr.expr.Expr.take_every/Vi-1_py-0.20.2.py",
  "new_file": "polars.expr.expr.Expr.take_every/Vi_py-0.20.3.py",
  "lines_added": 2,
  "lines_removed": 2
}
```
