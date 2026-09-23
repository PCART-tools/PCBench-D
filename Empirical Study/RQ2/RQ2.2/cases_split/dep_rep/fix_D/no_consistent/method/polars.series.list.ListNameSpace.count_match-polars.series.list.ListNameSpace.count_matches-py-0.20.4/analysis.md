# 一、突变情况分析

- **Total**: 456
- **替代API**: `polars.series.list.ListNameSpace.count_matches`
- **10% 阈值**: 45.6

## Vi-1 (py-0.19.2-py-0.20.4)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 1 | 1.0000 |
| tokenBased | 2 | 0.8500 |
| treeBased | 1 | 0.9783 |

## Vi (py-0.19.2-py-0.20.5)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 1 | 1.0000 |
| tokenBased | 144 | 0.1600 |
| treeBased | 89 | 0.4688 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 1 | 1 | +0 | false |
| tokenBased | 2 | 144 | -142 | true |
| treeBased | 1 | 89 | -88 | true |

```json
{
  "total": 456,
  "replacement_api": "polars.series.list.ListNameSpace.count_matches",
  "threshold_10pct": 45.6,
  "vi_minus_1": {
    "mapBased": {
      "rank": 1,
      "score": 1.0
    },
    "tokenBased": {
      "rank": 2,
      "score": 0.85
    },
    "treeBased": {
      "rank": 1,
      "score": 0.978261
    }
  },
  "vi": {
    "mapBased": {
      "rank": 1,
      "score": 1.0
    },
    "tokenBased": {
      "rank": 144,
      "score": 0.16
    },
    "treeBased": {
      "rank": 89,
      "score": 0.46875
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 1,
      "vi_rank": 1,
      "delta": 0,
      "exceeds_10pct": false
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 2,
      "vi_rank": 144,
      "delta": -142,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 1,
      "vi_rank": 89,
      "delta": -88,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `R_candidates/Vi-1_py-0.20.4/polars.series.list.ListNameSpace.count_matches.py`
- **new**: `R_candidates/Vi_py-0.20.5/polars.series.list.ListNameSpace.count_matches.py`
- **+1 / -3**

```diff
--- R_candidates/Vi-1_py-0.20.4/polars.series.list.ListNameSpace.count_matches.py
+++ R_candidates/Vi_py-0.20.5/polars.series.list.ListNameSpace.count_matches.py
@@ -1,4 +1,2 @@
-    def count_matches(
-        self, element: float | str | bool | int | date | datetime | time | Expr
-    ) -> Expr:
+    def count_matches(self, element: IntoExpr) -> Series:
         
```

```json
{
  "old_file": "R_candidates/Vi-1_py-0.20.4/polars.series.list.ListNameSpace.count_matches.py",
  "new_file": "R_candidates/Vi_py-0.20.5/polars.series.list.ListNameSpace.count_matches.py",
  "lines_added": 1,
  "lines_removed": 3
}
```
