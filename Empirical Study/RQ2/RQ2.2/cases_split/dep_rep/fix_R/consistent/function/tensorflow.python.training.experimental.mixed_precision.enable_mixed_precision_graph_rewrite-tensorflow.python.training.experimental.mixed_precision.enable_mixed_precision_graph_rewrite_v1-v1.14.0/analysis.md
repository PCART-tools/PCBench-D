# 一、突变情况分析

- **Total**: 22
- **替代API**: `tensorflow.python.training.experimental.mixed_precision.enable_mixed_precision_graph_rewrite_v1`
- **10% 阈值**: 2.2

## Vi-1 (v1.14.0-v2.6.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 1 | 0.8128 |
| tokenBased | 1 | 0.7288 |
| treeBased | 1 | 0.8137 |

## Vi (v2.0.0-v2.6.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 12 | 0.4877 |
| tokenBased | 4 | 0.3729 |
| treeBased | 16 | 0.4125 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 1 | 12 | -11 | true |
| tokenBased | 1 | 4 | -3 | true |
| treeBased | 1 | 16 | -15 | true |

```json
{
  "total": 22,
  "replacement_api": "tensorflow.python.training.experimental.mixed_precision.enable_mixed_precision_graph_rewrite_v1",
  "threshold_10pct": 2.2,
  "vi_minus_1": {
    "mapBased": {
      "rank": 1,
      "score": 0.812849
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.728814
    },
    "treeBased": {
      "rank": 1,
      "score": 0.813725
    }
  },
  "vi": {
    "mapBased": {
      "rank": 12,
      "score": 0.487715
    },
    "tokenBased": {
      "rank": 4,
      "score": 0.372881
    },
    "treeBased": {
      "rank": 16,
      "score": 0.4125
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 1,
      "vi_rank": 12,
      "delta": -11,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 1,
      "vi_rank": 4,
      "delta": -3,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 1,
      "vi_rank": 16,
      "delta": -15,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `tensorflow.python.training.experimental.mixed_precision.enable_mixed_precision_graph_rewrite/Vi-1_v1.14.0.py`
- **new**: `tensorflow.python.training.experimental.mixed_precision.enable_mixed_precision_graph_rewrite/Vi_v2.0.0.py`
- **+3 / -13**

```diff
--- tensorflow.python.training.experimental.mixed_precision.enable_mixed_precision_graph_rewrite/Vi-1_v1.14.0.py
+++ tensorflow.python.training.experimental.mixed_precision.enable_mixed_precision_graph_rewrite/Vi_v2.0.0.py
@@ -1,15 +1,5 @@
-@tf_export(v1=['train.experimental.enable_mixed_precision_graph_rewrite'])
+@tf_export('train.experimental.enable_mixed_precision_graph_rewrite', v1=[])
 def enable_mixed_precision_graph_rewrite(opt, loss_scale='dynamic'):
   
-
-
-  if mixed_precision_global_state.non_mixed_precision_session_created:
-
-
-    tf_logging.warn('You already have existing Sessions that do not use mixed '
-                    'precision. enable_mixed_precision_graph_rewrite() will '
-                    'not affect these Sessions.')
-  opt = _wrap_optimizer(opt, loss_scale)
-  config.set_optimizer_experimental_options({'auto_mixed_precision': True})
-  mixed_precision_global_state.mixed_precision_is_enabled = True
-  return opt
+  return _enable_mixed_precision_graph_rewrite_base(opt, loss_scale,
+                                                    use_v1_behavior=False)
```

```json
{
  "old_file": "tensorflow.python.training.experimental.mixed_precision.enable_mixed_precision_graph_rewrite/Vi-1_v1.14.0.py",
  "new_file": "tensorflow.python.training.experimental.mixed_precision.enable_mixed_precision_graph_rewrite/Vi_v2.0.0.py",
  "lines_added": 3,
  "lines_removed": 13
}
```
