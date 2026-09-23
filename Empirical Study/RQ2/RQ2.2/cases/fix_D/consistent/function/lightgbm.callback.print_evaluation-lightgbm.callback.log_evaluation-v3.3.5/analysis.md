# 一、突变情况分析

- **Total**: 70
- **替代API**: `lightgbm.callback.log_evaluation`
- **10% 阈值**: 7.0

## Vi-1 (v3.2.1-v3.3.5)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 1 | 1.0000 |
| tokenBased | 1 | 0.8800 |
| treeBased | 1 | 0.9583 |

## Vi (v3.2.1-v4.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 2 | 0.7877 |
| tokenBased | 16 | 0.2840 |
| treeBased | 26 | 0.3804 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 1 | 2 | -1 | false |
| tokenBased | 1 | 16 | -15 | true |
| treeBased | 1 | 26 | -25 | true |

```json
{
  "total": 70,
  "replacement_api": "lightgbm.callback.log_evaluation",
  "threshold_10pct": 7.0,
  "vi_minus_1": {
    "mapBased": {
      "rank": 1,
      "score": 1.0
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.88
    },
    "treeBased": {
      "rank": 1,
      "score": 0.958333
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
      "vi1_rank": 1,
      "vi_rank": 2,
      "delta": -1,
      "exceeds_10pct": false
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 1,
      "vi_rank": 16,
      "delta": -15,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 1,
      "vi_rank": 26,
      "delta": -25,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `R_candidates/Vi-1_v3.3.5/lightgbm.callback.log_evaluation.py`
- **new**: `R_candidates/Vi_v4.0.0/lightgbm.callback.log_evaluation.py`
- **+2 / -7**

```diff
--- R_candidates/Vi-1_v3.3.5/lightgbm.callback.log_evaluation.py
+++ R_candidates/Vi_v4.0.0/lightgbm.callback.log_evaluation.py
@@ -1,8 +1,3 @@
-def log_evaluation(period: int = 1, show_stdv: bool = True) -> Callable:
+def log_evaluation(period: int = 1, show_stdv: bool = True) -> _LogEvaluationCallback:
     
-    def _callback(env: CallbackEnv) -> None:
-        if period > 0 and env.evaluation_result_list and (env.iteration + 1) % period == 0:
-            result = '\t'.join([_format_eval_result(x, show_stdv) for x in env.evaluation_result_list])
-            _log_info(f'[{env.iteration + 1}]\t{result}')
-    _callback.order = 10
-    return _callback
+    return _LogEvaluationCallback(period=period, show_stdv=show_stdv)
```

```json
{
  "old_file": "R_candidates/Vi-1_v3.3.5/lightgbm.callback.log_evaluation.py",
  "new_file": "R_candidates/Vi_v4.0.0/lightgbm.callback.log_evaluation.py",
  "lines_added": 2,
  "lines_removed": 7
}
```
