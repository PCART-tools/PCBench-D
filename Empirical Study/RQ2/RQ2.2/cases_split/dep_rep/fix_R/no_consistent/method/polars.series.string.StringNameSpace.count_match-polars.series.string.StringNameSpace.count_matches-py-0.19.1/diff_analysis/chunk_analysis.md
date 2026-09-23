# Diff 分块分析：py-polars.polars.series.string.StringNameSpace.count_match-py-polars.polars.series.string.StringNameSpace.count_matches-py-0.19.1
## 文件定位

- 旧文件：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/consistent/method/py-polars.polars.series.string.StringNameSpace.count_match-py-polars.polars.series.string.StringNameSpace.count_matches-py-0.19.1/py-polars.polars.series.string.StringNameSpace.count_match/Vi-1_py-0.19.1.py
- 新文件：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/consistent/method/py-polars.polars.series.string.StringNameSpace.count_match-py-polars.polars.series.string.StringNameSpace.count_matches-py-0.19.1/py-polars.polars.series.string.StringNameSpace.count_match/Vi_py-0.19.2.py
- 目标文件（Target）：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/consistent/method/py-polars.polars.series.string.StringNameSpace.count_match-py-polars.polars.series.string.StringNameSpace.count_matches-py-0.19.1/R_candidates/py-1.0.0/py-polars.polars.series.string.StringNameSpace.count_matches.py
- 实验组：fix_R
- 总变更：+9 / -6 行
- 分块数：6

## Block 1 — block_001.patch
定位：@@ -1,2 +1,2 @@
说明：def count_match(self, pattern: str) -> Series:、def count_match(self, pattern: str | Series) -> Series:

## Block 2 — block_002.patch
定位：@@ -8,3 +8,4 @@
说明：<https://docs.rs/regex/latest/regex/>`_.、<https://docs.rs/regex/latest/regex/>`_. Can also be a :clas、regular expressions.

## Block 3 — block_003.patch
定位：@@ -13,4 +14,4 @@
说明：Series of data type :class:`UInt32`. Contains null values if、value is null or if the regex captures nothing.、Series of data type :class:`UInt32`. Returns null if the ori...

## Block 4 — block_004.patch
定位：@@ -18,3 +19,3 @@
说明：>>> s = pl.Series("foo", ["123 bla 45 asd", "xyz 678 910t"])、>>> s = pl.Series("foo", ["123 bla 45 asd", "xyz 678 910t", 

## Block 5 — block_005.patch
定位：@@ -21,3 +22,3 @@
说明：shape: (2,)、shape: (4,)

## Block 6 — block_006.patch
定位：@@ -26,2 +27,4 @@
说明：0、null
