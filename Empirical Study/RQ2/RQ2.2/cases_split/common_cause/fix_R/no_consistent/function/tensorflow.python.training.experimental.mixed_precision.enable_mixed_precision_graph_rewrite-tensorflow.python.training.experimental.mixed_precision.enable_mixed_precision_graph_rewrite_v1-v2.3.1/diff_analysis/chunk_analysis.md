# Diff 分块分析：tensorflow.python.training.experimental.mixed_precision.enable_mixed_precision_graph_rewrite-tensorflow.python.training.experimental.mixed_precision.enable_mixed_precision_graph_rewrite_v1-v2.3.1
## 文件定位

- 旧文件：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/consistent/function/tensorflow.python.training.experimental.mixed_precision.enable_mixed_precision_graph_rewrite-tensorflow.python.training.experimental.mixed_precision.enable_mixed_precision_graph_rewrite_v1-v2.3.1/tensorflow.python.training.experimental.mixed_precision.enable_mixed_precision_graph_rewrite/Vi-1_v2.3.1.py
- 新文件：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/consistent/function/tensorflow.python.training.experimental.mixed_precision.enable_mixed_precision_graph_rewrite-tensorflow.python.training.experimental.mixed_precision.enable_mixed_precision_graph_rewrite_v1-v2.3.1/tensorflow.python.training.experimental.mixed_precision.enable_mixed_precision_graph_rewrite/Vi_v2.4.0.py
- 目标文件（Target）：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/consistent/function/tensorflow.python.training.experimental.mixed_precision.enable_mixed_precision_graph_rewrite-tensorflow.python.training.experimental.mixed_precision.enable_mixed_precision_graph_rewrite_v1-v2.3.1/R_candidates/v2.6.0/tensorflow.python.training.experimental.mixed_precision.enable_mixed_precision_graph_rewrite_v1.py
- 实验组：fix_R
- 总变更：+9 / -3 行
- 分块数：4

## Block 1 — block_001.patch
定位：@@ -1,1 +1,7 @@
说明：@deprecation.deprecated(、'2020-11-30',、'Use tf.keras.mixed_precision. There is a guide at '...

## Block 2 — block_002.patch
定位：@@ -61,3 +67,3 @@
说明：* `WhiteList`: Ops that are considered numerically safe for 、* `AllowList`: Ops that are considered numerically safe for 

## Block 3 — block_003.patch
定位：@@ -63,3 +69,3 @@
说明：* `BlackList`: Ops that are numerically unsafe to execute in、* `DenyList`: Ops that are numerically unsafe to execute in 

## Block 4 — block_004.patch
定位：@@ -66,3 +72,3 @@
说明：float16 unless downstream from a BlackList Op. E.g. `Add` an、float16 unless downstream from a DenyList Op. E.g. `Add` and
