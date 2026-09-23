# 一、突变情况分析

- **Total**: 120
- **替代API**: `polars.lazyframe.frame.LazyFrame.shift`
- **10% 阈值**: 12.0

## Vi-1 (py-0.19.11-py-1.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 11 | 0.7470 |
| tokenBased | 3 | 0.4020 |
| treeBased | 9 | 0.5979 |

## Vi (py-0.19.12-py-1.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 74 | 0.6029 |
| tokenBased | 3 | 0.2917 |
| treeBased | 20 | 0.5000 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 11 | 74 | -63 | true |
| tokenBased | 3 | 3 | +0 | false |
| treeBased | 9 | 20 | -11 | false |

```json
{
  "total": 120,
  "replacement_api": "polars.lazyframe.frame.LazyFrame.shift",
  "threshold_10pct": 12.0,
  "vi_minus_1": {
    "mapBased": {
      "rank": 11,
      "score": 0.746994
    },
    "tokenBased": {
      "rank": 3,
      "score": 0.401961
    },
    "treeBased": {
      "rank": 9,
      "score": 0.597938
    }
  },
  "vi": {
    "mapBased": {
      "rank": 74,
      "score": 0.602871
    },
    "tokenBased": {
      "rank": 3,
      "score": 0.291667
    },
    "treeBased": {
      "rank": 20,
      "score": 0.5
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 11,
      "vi_rank": 74,
      "delta": -63,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 3,
      "vi_rank": 3,
      "delta": 0,
      "exceeds_10pct": false
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 9,
      "vi_rank": 20,
      "delta": -11,
      "exceeds_10pct": false
    }
  ]
}
```

# 二、old → new Diff

- **old**: `polars.lazyframe.frame.LazyFrame.shift_and_fill/Vi-1_py-0.19.11.py`
- **new**: `polars.lazyframe.frame.LazyFrame.shift_and_fill/Vi_py-0.19.12.py`
- **+2 / -3**

```diff
--- polars.lazyframe.frame.LazyFrame.shift_and_fill/Vi-1_py-0.19.11.py
+++ polars.lazyframe.frame.LazyFrame.shift_and_fill/Vi_py-0.19.12.py
@@ -1,3 +1,4 @@
+    @deprecate_function("Use `shift` instead.", version="0.19.12")
     @deprecate_renamed_parameter("periods", "n", version="0.19.11")
     def shift_and_fill(
         self,
@@ -6,6 +7,4 @@
         n: int = 1,
     ) -> Self:
         
-        if not isinstance(fill_value, pl.Expr):
-            fill_value = F.lit(fill_value)
-        return self._from_pyldf(self._ldf.shift_and_fill(n, fill_value._pyexpr))
+        return self.shift(n, fill_value=fill_value)
```

```json
{
  "old_file": "polars.lazyframe.frame.LazyFrame.shift_and_fill/Vi-1_py-0.19.11.py",
  "new_file": "polars.lazyframe.frame.LazyFrame.shift_and_fill/Vi_py-0.19.12.py",
  "lines_added": 2,
  "lines_removed": 3
}
```
