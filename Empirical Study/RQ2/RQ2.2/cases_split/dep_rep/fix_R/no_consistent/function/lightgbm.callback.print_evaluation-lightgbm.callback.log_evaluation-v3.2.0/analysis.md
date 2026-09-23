# 一、突变情况分析

- **Total**: 74
- **替代API**: `lightgbm.callback.log_evaluation`
- **10% 阈值**: 7.4

## Vi-1 (v3.2.0-v4.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 2 | 0.7877 |
| tokenBased | 42 | 0.1948 |
| treeBased | 41 | 0.3333 |

## Vi (v3.2.1-v4.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 2 | 0.7877 |
| tokenBased | 16 | 0.2840 |
| treeBased | 26 | 0.3804 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 2 | 2 | +0 | false |
| tokenBased | 42 | 16 | +26 | true |
| treeBased | 41 | 26 | +15 | true |

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
      "rank": 42,
      "score": 0.194805
    },
    "treeBased": {
      "rank": 41,
      "score": 0.333333
    }
  },
  "vi": {
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
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 2,
      "vi_rank": 2,
      "delta": 0,
      "exceeds_10pct": false
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 42,
      "vi_rank": 16,
      "delta": 26,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 41,
      "vi_rank": 26,
      "delta": 15,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `lightgbm.callback.print_evaluation/Vi-1_v3.2.0.py`
- **new**: `lightgbm.callback.print_evaluation/Vi_v3.2.1.py`
- **+2 / -2**

```diff
--- lightgbm.callback.print_evaluation/Vi-1_v3.2.0.py
+++ lightgbm.callback.print_evaluation/Vi_v3.2.1.py
@@ -1,6 +1,6 @@
-def print_evaluation(period=1, show_stdv=True):
+def print_evaluation(period: int = 1, show_stdv: bool = True) -> Callable:
     
-    def _callback(env):
+    def _callback(env: CallbackEnv) -> None:
         if period > 0 and env.evaluation_result_list and (env.iteration + 1) % period == 0:
             result = '\t'.join([_format_eval_result(x, show_stdv) for x in env.evaluation_result_list])
             _log_info('[%d]\t%s' % (env.iteration + 1, result))
```

```json
{
  "old_file": "lightgbm.callback.print_evaluation/Vi-1_v3.2.0.py",
  "new_file": "lightgbm.callback.print_evaluation/Vi_v3.2.1.py",
  "lines_added": 2,
  "lines_removed": 2
}
```
