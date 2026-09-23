# 一、突变情况分析

- **Total**: 22
- **替代API**: `tensorflow.python.training.experimental.mixed_precision.enable_mixed_precision_graph_rewrite_v1`
- **10% 阈值**: 2.2

## Vi-1 (v2.3.1-v2.6.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 12 | 0.4877 |
| tokenBased | 4 | 0.3729 |
| treeBased | 16 | 0.4125 |

## Vi (v2.4.0-v2.6.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 12 | 0.4877 |
| tokenBased | 4 | 0.3667 |
| treeBased | 9 | 0.4706 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 12 | 12 | +0 | false |
| tokenBased | 4 | 4 | +0 | false |
| treeBased | 16 | 9 | +7 | true |

```json
{
  "total": 22,
  "replacement_api": "tensorflow.python.training.experimental.mixed_precision.enable_mixed_precision_graph_rewrite_v1",
  "threshold_10pct": 2.2,
  "vi_minus_1": {
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
  "vi": {
    "mapBased": {
      "rank": 12,
      "score": 0.487715
    },
    "tokenBased": {
      "rank": 4,
      "score": 0.366667
    },
    "treeBased": {
      "rank": 9,
      "score": 0.470588
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 12,
      "vi_rank": 12,
      "delta": 0,
      "exceeds_10pct": false
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 4,
      "vi_rank": 4,
      "delta": 0,
      "exceeds_10pct": false
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 16,
      "vi_rank": 9,
      "delta": 7,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `tensorflow.python.training.experimental.mixed_precision.enable_mixed_precision_graph_rewrite/Vi-1_v2.3.1.py`
- **new**: `tensorflow.python.training.experimental.mixed_precision.enable_mixed_precision_graph_rewrite/Vi_v2.4.0.py`
- **+6 / -0**

```diff
--- tensorflow.python.training.experimental.mixed_precision.enable_mixed_precision_graph_rewrite/Vi-1_v2.3.1.py
+++ tensorflow.python.training.experimental.mixed_precision.enable_mixed_precision_graph_rewrite/Vi_v2.4.0.py
@@ -1,3 +1,9 @@
+@deprecation.deprecated(
+    '2020-11-30',
+    'Use tf.keras.mixed_precision. There is a guide at '
+    'https://www.tensorflow.org/guide/mixed_precision. Alternatively, '
+    '`tf.compat.v1.mixed_precision.enable_mixed_precision_graph_rewrite` can '
+    'be used, but this is not recommended for TF2 code.')
 @tf_export('train.experimental.enable_mixed_precision_graph_rewrite', v1=[])
 def enable_mixed_precision_graph_rewrite(opt, loss_scale='dynamic'):
   
```

```json
{
  "old_file": "tensorflow.python.training.experimental.mixed_precision.enable_mixed_precision_graph_rewrite/Vi-1_v2.3.1.py",
  "new_file": "tensorflow.python.training.experimental.mixed_precision.enable_mixed_precision_graph_rewrite/Vi_v2.4.0.py",
  "lines_added": 6,
  "lines_removed": 0
}
```
