# Diff 分块分析：py-polars.polars.expr.string.ExprStringNameSpace.json_extract-py-polars.polars.expr.string.ExprStringNameSpace.json_decode-py-0.19.14
## 文件定位

- 旧文件：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/consistent/method/py-polars.polars.expr.string.ExprStringNameSpace.json_extract-py-polars.polars.expr.string.ExprStringNameSpace.json_decode-py-0.19.14/py-polars.polars.expr.string.ExprStringNameSpace.json_extract/Vi-1_py-0.19.14.py
- 新文件：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/consistent/method/py-polars.polars.expr.string.ExprStringNameSpace.json_extract-py-polars.polars.expr.string.ExprStringNameSpace.json_decode-py-0.19.14/py-polars.polars.expr.string.ExprStringNameSpace.json_extract/Vi_py-0.19.15.py
- 目标文件（Target）：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/consistent/method/py-polars.polars.expr.string.ExprStringNameSpace.json_extract-py-polars.polars.expr.string.ExprStringNameSpace.json_decode-py-0.19.14/R_candidates/py-1.0.0/py-polars.polars.expr.string.ExprStringNameSpace.json_decode.py
- 实验组：fix_R
- 总变更：+4 / -28 行
- 分块数：4

## Block 1 — block_001.patch
定位：@@ -1,1 +1,2 @@
说明：@deprecate_renamed_function("json_decode", version="0.19.12"

## Block 2 — block_002.patch
定位：@@ -6,3 +7,4 @@
说明：Throw errors if encounter invalid JSON strings.、.. deprecated:: 0.19.15、This method has been renamed to :meth:`json_decode`.

## Block 3 — block_003.patch
定位：@@ -16,26 +18,2 @@
说明：、See Also、--------...

## Block 4 — block_004.patch
定位：@@ -41,4 +19,2 @@
说明：if dtype is not None:、dtype = py_type_to_dtype(dtype)、return wrap_expr(self._pyexpr.str_json_extract(dtype, infer_...
