# 一、突变情况分析

- **Total**: 120
- **替代API**: `polars.lazyframe.frame.LazyFrame.gather_every`
- **10% 阈值**: 12.0

## Vi-1 (py-0.20.2-py-1.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 10 | 0.9035 |
| tokenBased | 3 | 0.3778 |
| treeBased | 54 | 0.5682 |

## Vi (py-0.20.3-py-1.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 1 | 1.0000 |
| tokenBased | 1 | 0.5333 |
| treeBased | 3 | 0.7143 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 10 | 1 | +9 | false |
| tokenBased | 3 | 1 | +2 | false |
| treeBased | 54 | 3 | +51 | true |

```json
{
  "total": 120,
  "replacement_api": "polars.lazyframe.frame.LazyFrame.gather_every",
  "threshold_10pct": 12.0,
  "vi_minus_1": {
    "mapBased": {
      "rank": 10,
      "score": 0.903475
    },
    "tokenBased": {
      "rank": 3,
      "score": 0.377778
    },
    "treeBased": {
      "rank": 54,
      "score": 0.568182
    }
  },
  "vi": {
    "mapBased": {
      "rank": 1,
      "score": 1.0
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.533333
    },
    "treeBased": {
      "rank": 3,
      "score": 0.714286
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 10,
      "vi_rank": 1,
      "delta": 9,
      "exceeds_10pct": false
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 3,
      "vi_rank": 1,
      "delta": 2,
      "exceeds_10pct": false
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 54,
      "vi_rank": 3,
      "delta": 51,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `polars.lazyframe.frame.LazyFrame.take_every/Vi-1_py-0.20.2.py`
- **new**: `polars.lazyframe.frame.LazyFrame.take_every/Vi_py-0.20.3.py`
- **+2 / -2**

```diff
--- polars.lazyframe.frame.LazyFrame.take_every/Vi-1_py-0.20.2.py
+++ polars.lazyframe.frame.LazyFrame.take_every/Vi_py-0.20.3.py
@@ -1,4 +1,4 @@
     @deprecate_renamed_function("gather_every", version="0.19.14")
-    def take_every(self, n: int) -> Self:
+    def take_every(self, n: int, offset: int = 0) -> Self:
         
-        return self.gather_every(n)
+        return self.gather_every(n, offset)
```

```json
{
  "old_file": "polars.lazyframe.frame.LazyFrame.take_every/Vi-1_py-0.20.2.py",
  "new_file": "polars.lazyframe.frame.LazyFrame.take_every/Vi_py-0.20.3.py",
  "lines_added": 2,
  "lines_removed": 2
}
```
