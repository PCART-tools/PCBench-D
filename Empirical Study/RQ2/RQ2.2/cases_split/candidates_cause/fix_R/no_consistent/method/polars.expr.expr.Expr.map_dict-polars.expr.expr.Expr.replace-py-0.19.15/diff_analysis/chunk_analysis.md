# Diff 分块分析：py-polars.polars.expr.expr.Expr.map_dict-py-polars.polars.expr.expr.Expr.replace-py-0.19.15
## 文件定位

- 旧文件：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/consistent/method/py-polars.polars.expr.expr.Expr.map_dict-py-polars.polars.expr.expr.Expr.replace-py-0.19.15/py-polars.polars.expr.expr.Expr.map_dict/Vi-1_py-0.19.15.py
- 新文件：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/consistent/method/py-polars.polars.expr.expr.Expr.map_dict-py-polars.polars.expr.expr.Expr.replace-py-0.19.15/py-polars.polars.expr.expr.Expr.map_dict/Vi_py-0.19.16.py
- 目标文件（Target）：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/consistent/method/py-polars.polars.expr.expr.Expr.map_dict-py-polars.polars.expr.expr.Expr.replace-py-0.19.15/R_candidates/py-1.0.0/py-polars.polars.expr.expr.Expr.replace.py
- 实验组：fix_R
- 总变更：+14 / -343 行
- 分块数：6

## Block 1 — block_001.patch
定位：@@ -1,1 +1,8 @@
说明：@deprecate_function(、"It has been renamed to `replace`."、" The default behavior has changed to keep any values not pr...

## Block 2 — block_002.patch
定位：@@ -2,3 +9,3 @@
说明：remapping: dict[Any, Any],、mapping: dict[Any, Any],

## Block 3 — block_003.patch
定位：@@ -10,4 +17,6 @@
说明：Needs a global string cache for lazily evaluated queries on 、type `pl.Categorical`.、.. deprecated:: 0.19.16...

## Block 4 — block_004.patch
定位：@@ -15,3 +24,3 @@
说明：remapping、mapping

## Block 5 — block_005.patch
定位：@@ -24,145 +33,2 @@
说明：See Also、--------、map...

## Block 6 — block_006.patch
定位：@@ -168,197 +34,2 @@
说明：、def _remap_key_or_value_series(、name: str,...
