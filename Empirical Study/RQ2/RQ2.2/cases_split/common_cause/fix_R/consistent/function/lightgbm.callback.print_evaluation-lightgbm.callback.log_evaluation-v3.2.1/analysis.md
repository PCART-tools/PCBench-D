# 一、突变情况分析

- **Total**: 74
- **替代API**: `lightgbm.callback.log_evaluation`
- **10% 阈值**: 7.4

## Vi-1 (v3.2.1-v4.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 2 | 0.7877 |
| tokenBased | 16 | 0.2840 |
| treeBased | 26 | 0.3804 |

## Vi (v3.3.0-v4.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 1 | 0.9213 |
| tokenBased | 1 | 0.5349 |
| treeBased | 1 | 0.8478 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 2 | 1 | +1 | false |
| tokenBased | 16 | 1 | +15 | true |
| treeBased | 26 | 1 | +25 | true |

```json
{
  "total": 74,
  "replacement_api": "lightgbm.callback.log_evaluation",
  "threshold_10pct": 7.4,
  "vi_minus_1": {
    "mapBased": {
      "rank": 2,
      "score": 0.787698
    },
    "tokenBased": {
      "rank": 16,
      "score": 0.283951
    },
    "treeBased": {
      "rank": 26,
      "score": 0.380435
    }
  },
  "vi": {
    "mapBased": {
      "rank": 1,
      "score": 0.92126
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.534884
    },
    "treeBased": {
      "rank": 1,
      "score": 0.847826
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 2,
      "vi_rank": 1,
      "delta": 1,
      "exceeds_10pct": false
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 16,
      "vi_rank": 1,
      "delta": 15,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 26,
      "vi_rank": 1,
      "delta": 25,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `lightgbm.callback.print_evaluation/Vi-1_v3.2.1.py`
- **new**: `lightgbm.callback.print_evaluation/Vi_v3.3.0.py`
- **+3 / -6**

```diff
--- lightgbm.callback.print_evaluation/Vi-1_v3.2.1.py
+++ lightgbm.callback.print_evaluation/Vi_v3.3.0.py
@@ -1,8 +1,5 @@
 def print_evaluation(period: int = 1, show_stdv: bool = True) -> Callable:
     
-    def _callback(env: CallbackEnv) -> None:
-        if period > 0 and env.evaluation_result_list and (env.iteration + 1) % period == 0:
-            result = '\t'.join([_format_eval_result(x, show_stdv) for x in env.evaluation_result_list])
-            _log_info('[%d]\t%s' % (env.iteration + 1, result))
-    _callback.order = 10
-    return _callback
+    _log_warning("'print_evaluation()' callback is deprecated and will be removed in a future release of LightGBM. "
+                 "Use 'log_evaluation()' callback instead.")
+    return log_evaluation(period=period, show_stdv=show_stdv)
```

```json
{
  "old_file": "lightgbm.callback.print_evaluation/Vi-1_v3.2.1.py",
  "new_file": "lightgbm.callback.print_evaluation/Vi_v3.3.0.py",
  "lines_added": 3,
  "lines_removed": 6
}
```
