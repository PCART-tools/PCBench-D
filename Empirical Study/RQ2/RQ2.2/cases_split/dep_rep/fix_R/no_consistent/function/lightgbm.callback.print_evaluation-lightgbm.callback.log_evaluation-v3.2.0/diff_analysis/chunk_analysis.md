# Diff 分块分析：python-package.lightgbm.callback.print_evaluation-python-package.lightgbm.callback.log_evaluation-v3.2.0
## 文件定位

- 旧文件：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/consistent/function/python-package.lightgbm.callback.print_evaluation-python-package.lightgbm.callback.log_evaluation-v3.2.0/python-package.lightgbm.callback.print_evaluation/Vi-1_v3.2.0.py
- 新文件：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/consistent/function/python-package.lightgbm.callback.print_evaluation-python-package.lightgbm.callback.log_evaluation-v3.2.0/python-package.lightgbm.callback.print_evaluation/Vi_v3.2.1.py
- 目标文件（Target）：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/consistent/function/python-package.lightgbm.callback.print_evaluation-python-package.lightgbm.callback.log_evaluation-v3.2.0/R_candidates/v4.0.0/python-package.lightgbm.callback.log_evaluation.py
- 实验组：fix_R
- 总变更：+3 / -3 行
- 分块数：3

## Block 1 — block_001.patch
定位：@@ -1,2 +1,2 @@
说明：def print_evaluation(period=1, show_stdv=True):、def print_evaluation(period: int = 1, show_stdv: bool = True

## Block 2 — block_002.patch
定位：@@ -15,3 +15,3 @@
说明：def _callback(env):、def _callback(env: CallbackEnv) -> None:

## Block 3 — block_003.patch
定位：@@ -19,3 +19,3 @@
说明：_callback.order = 10、_callback.order = 10  # type: ignore
