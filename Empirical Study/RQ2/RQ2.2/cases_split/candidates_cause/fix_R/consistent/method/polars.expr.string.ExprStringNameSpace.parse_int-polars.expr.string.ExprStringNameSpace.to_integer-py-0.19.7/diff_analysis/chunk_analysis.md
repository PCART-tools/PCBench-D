# Diff 分块分析：py-polars.polars.expr.string.ExprStringNameSpace.parse_int-py-polars.polars.expr.string.ExprStringNameSpace.to_integer-py-0.19.7
## 文件定位

- 旧文件：/media/he/Rbench/similarity/RQ2/split2.0/candidates_cause/fix_R/consistent/method/py-polars.polars.expr.string.ExprStringNameSpace.parse_int-py-polars.polars.expr.string.ExprStringNameSpace.to_integer-py-0.19.7/py-polars.polars.expr.string.ExprStringNameSpace.parse_int/Vi-1_py-0.19.7.py
- 新文件：/media/he/Rbench/similarity/RQ2/split2.0/candidates_cause/fix_R/consistent/method/py-polars.polars.expr.string.ExprStringNameSpace.parse_int-py-polars.polars.expr.string.ExprStringNameSpace.to_integer-py-0.19.7/py-polars.polars.expr.string.ExprStringNameSpace.parse_int/Vi_py-0.19.8.py
- 目标文件（Target）：/media/he/Rbench/similarity/RQ2/split2.0/candidates_cause/fix_R/consistent/method/py-polars.polars.expr.string.ExprStringNameSpace.parse_int-py-polars.polars.expr.string.ExprStringNameSpace.to_integer-py-0.19.7/R_candidates/py-1.0.0/py-polars.polars.expr.string.ExprStringNameSpace.to_integer.py
- 实验组：fix_R
- 总变更：+10 / -4 行
- 分块数：4

## Block 1 — block_001.patch
定位：@@ -1,2 +1,2 @@
说明：def parse_int(self, radix: int = 2, *, strict: bool = True) 、def parse_int(self, radix: int | None = None, *, strict: boo

## Block 2 — block_002.patch
定位：@@ -4,3 +4,3 @@
说明：By default base 2. ParseError/Overflows become Nulls.、ParseError/Overflows become Nulls.

## Block 3 — block_003.patch
定位：@@ -10,4 +10,2 @@
说明：Default: 2.、

## Block 4 — block_004.patch
定位：@@ -52,2 +50,10 @@
说明：if radix is None:、issue_deprecation_warning(、"The default value for the `radix` parameter of `parse_int` ...
