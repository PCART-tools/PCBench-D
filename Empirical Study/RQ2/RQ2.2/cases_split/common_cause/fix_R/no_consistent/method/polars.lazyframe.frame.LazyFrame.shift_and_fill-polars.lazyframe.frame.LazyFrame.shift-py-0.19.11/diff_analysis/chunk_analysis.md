# Diff 分块分析：py-polars.polars.lazyframe.frame.LazyFrame.shift_and_fill-py-polars.polars.lazyframe.frame.LazyFrame.shift-py-0.19.11
## 文件定位

- 旧文件：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/consistent/method/py-polars.polars.lazyframe.frame.LazyFrame.shift_and_fill-py-polars.polars.lazyframe.frame.LazyFrame.shift-py-0.19.11/py-polars.polars.lazyframe.frame.LazyFrame.shift_and_fill/Vi-1_py-0.19.11.py
- 新文件：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/consistent/method/py-polars.polars.lazyframe.frame.LazyFrame.shift_and_fill-py-polars.polars.lazyframe.frame.LazyFrame.shift-py-0.19.11/py-polars.polars.lazyframe.frame.LazyFrame.shift_and_fill/Vi_py-0.19.12.py
- 目标文件（Target）：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/consistent/method/py-polars.polars.lazyframe.frame.LazyFrame.shift_and_fill-py-polars.polars.lazyframe.frame.LazyFrame.shift-py-0.19.11/R_candidates/py-1.0.0/py-polars.polars.lazyframe.frame.LazyFrame.shift.py
- 实验组：fix_R
- 总变更：+5 / -34 行
- 分块数：4

## Block 1 — block_001.patch
定位：@@ -1,1 +1,2 @@
说明：@deprecate_function("Use `shift` instead.", version="0.19.12

## Block 2 — block_002.patch
定位：@@ -10,2 +11,5 @@
说明：.. deprecated:: 0.19.12、Use :func:`shift` instead.、

## Block 3 — block_003.patch
定位：@@ -17,33 +21,2 @@
说明：Examples、--------、>>> lf = pl.LazyFrame(...

## Block 4 — block_004.patch
定位：@@ -49,4 +22,2 @@
说明：if not isinstance(fill_value, pl.Expr):、fill_value = F.lit(fill_value)、return self._from_pyldf(self._ldf.shift_and_fill(n, fill_val...
