# Diff 分块分析：py-polars.polars.expr.list.ExprListNameSpace.count_match-py-polars.polars.expr.list.ExprListNameSpace.count_matches-py-0.19.2
## 文件定位

- 旧文件：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/consistent/method/py-polars.polars.expr.list.ExprListNameSpace.count_match-py-polars.polars.expr.list.ExprListNameSpace.count_matches-py-0.19.2/py-polars.polars.expr.list.ExprListNameSpace.count_match/Vi-1_py-0.19.2.py
- 新文件：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/consistent/method/py-polars.polars.expr.list.ExprListNameSpace.count_match-py-polars.polars.expr.list.ExprListNameSpace.count_matches-py-0.19.2/py-polars.polars.expr.list.ExprListNameSpace.count_match/Vi_py-0.19.3.py
- 目标文件（Target）：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/consistent/method/py-polars.polars.expr.list.ExprListNameSpace.count_match-py-polars.polars.expr.list.ExprListNameSpace.count_matches-py-0.19.2/R_candidates/py-1.0.0/py-polars.polars.expr.list.ExprListNameSpace.count_matches.py
- 实验组：fix_R
- 总变更：+5 / -19 行
- 分块数：4

## Block 1 — block_001.patch
定位：@@ -1,1 +1,2 @@
说明：@deprecate_renamed_function("count_matches", version="0.19.3

## Block 2 — block_002.patch
定位：@@ -3,2 +4,5 @@
说明：、.. deprecated:: 0.19.3、This method has been renamed to :func:`count_matches`.

## Block 3 — block_003.patch
定位：@@ -9,19 +13,2 @@
说明：Examples、--------、>>> df = pl.DataFrame({"listcol": [[0], [1], [1, 2, 3, 2], [...

## Block 4 — block_004.patch
定位：@@ -27,3 +14,2 @@
说明：element = parse_as_expression(element, str_as_lit=True)、return wrap_expr(self._pyexpr.list_count_match(element))、return self.count_matches(element)
