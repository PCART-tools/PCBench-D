# Diff 分块分析：python-package.lightgbm.callback.print_evaluation-python-package.lightgbm.callback.log_evaluation-v3.2.1
## 文件定位

- 旧文件：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/consistent/function/python-package.lightgbm.callback.print_evaluation-python-package.lightgbm.callback.log_evaluation-v3.2.1/python-package.lightgbm.callback.print_evaluation/Vi-1_v3.2.1.py
- 新文件：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/consistent/function/python-package.lightgbm.callback.print_evaluation-python-package.lightgbm.callback.log_evaluation-v3.2.1/python-package.lightgbm.callback.print_evaluation/Vi_v3.3.0.py
- 目标文件（Target）：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/consistent/function/python-package.lightgbm.callback.print_evaluation-python-package.lightgbm.callback.log_evaluation-v3.2.1/R_candidates/v4.0.0/python-package.lightgbm.callback.log_evaluation.py
- 实验组：fix_R
- 总变更：+5 / -18 行
- 分块数：3

## Block 1 — block_001.patch
定位：@@ -1,3 +1,3 @@
说明："""Create a callback that prints the evaluation results.、"""Create a callback that logs the evaluation results.

## Block 2 — block_002.patch
定位：@@ -3,13 +3,3 @@
说明：Parameters、----------、period : int, optional (default=1)...

## Block 3 — block_003.patch
定位：@@ -15,7 +5,4 @@
说明：def _callback(env: CallbackEnv) -> None:、if period > 0 and env.evaluation_result_list and (env.iterat、result = '\t'.join([_format_eval_result(x, show_stdv) for x ...
