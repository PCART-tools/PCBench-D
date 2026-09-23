# Diff 分块分析：py-polars.polars.expr.expr.Expr.shift_and_fill-py-polars.polars.expr.expr.Expr.shift-py-0.19.11
## 文件定位

- 旧文件：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/no_consistent/method/py-polars.polars.expr.expr.Expr.shift_and_fill-py-polars.polars.expr.expr.Expr.shift-py-0.19.11/py-polars.polars.expr.expr.Expr.shift_and_fill/Vi-1_py-0.19.11.py
- 新文件：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/no_consistent/method/py-polars.polars.expr.expr.Expr.shift_and_fill-py-polars.polars.expr.expr.Expr.shift-py-0.19.11/py-polars.polars.expr.expr.Expr.shift_and_fill/Vi_py-0.19.12.py
- 目标文件（Target）：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/no_consistent/method/py-polars.polars.expr.expr.Expr.shift_and_fill-py-polars.polars.expr.expr.Expr.shift-py-0.19.11/R_candidates/py-1.0.0/py-polars.polars.expr.expr.Expr.shift.py
- 实验组：fix_R
- 总变更：+5 / -18 行
- 分块数：4

## Block 1 — block_001.patch
定位：@@ -1,1 +1,2 @@
说明：@deprecate_function("Use `shift` instead.", version="0.19.12

## Block 2 — block_002.patch
定位：@@ -10,2 +11,5 @@
说明：.. deprecated:: 0.19.12、Use :func:`shift` instead.、

## Block 3 — block_003.patch
定位：@@ -17,18 +21,2 @@
说明：Examples、--------、>>> df = pl.DataFrame({"foo": [1, 2, 3, 4]})...

## Block 4 — block_004.patch
定位：@@ -34,3 +22,2 @@
说明：fill_value = parse_as_expression(fill_value, str_as_lit=True、return self._from_pyexpr(self._pyexpr.shift_and_fill(n, fill、return self.shift(n, fill_value=fill_value)
