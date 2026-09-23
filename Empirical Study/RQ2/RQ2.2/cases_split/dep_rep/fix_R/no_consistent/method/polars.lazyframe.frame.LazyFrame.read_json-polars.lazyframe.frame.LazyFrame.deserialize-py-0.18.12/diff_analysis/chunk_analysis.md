# Diff 分块分析：py-polars.polars.lazyframe.frame.LazyFrame.read_json-py-polars.polars.lazyframe.frame.LazyFrame.deserialize-py-0.18.12
## 文件定位

- 旧文件：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/consistent/method/py-polars.polars.lazyframe.frame.LazyFrame.read_json-py-polars.polars.lazyframe.frame.LazyFrame.deserialize-py-0.18.12/py-polars.polars.lazyframe.frame.LazyFrame.read_json/Vi-1_py-0.18.12.py
- 新文件：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/consistent/method/py-polars.polars.lazyframe.frame.LazyFrame.read_json-py-polars.polars.lazyframe.frame.LazyFrame.deserialize-py-0.18.12/py-polars.polars.lazyframe.frame.LazyFrame.read_json/Vi_py-0.18.13.py
- 目标文件（Target）：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/consistent/method/py-polars.polars.lazyframe.frame.LazyFrame.read_json-py-polars.polars.lazyframe.frame.LazyFrame.deserialize-py-0.18.12/R_candidates/py-0.20.0/py-polars.polars.lazyframe.frame.LazyFrame.deserialize.py
- 实验组：fix_R
- 总变更：+9 / -9 行
- 分块数：5

## Block 1 — block_001.patch
定位：@@ -1,3 +1,5 @@
说明：def read_json(cls, file: str | Path | IOBase) -> Self:、@deprecate_renamed_function("deserialize", version="0.18.12"、@deprecate_renamed_parameter("file", "source", version="0.18...

## Block 2 — block_002.patch
定位：@@ -5,2 +7,5 @@
说明：.. deprecated:: 0.18.12、This class method has been renamed to ``deserialize``.、

## Block 3 — block_003.patch
定位：@@ -7,3 +12,3 @@
说明：file、source

## Block 4 — block_004.patch
定位：@@ -12,3 +17,3 @@
说明：LazyFrame.from_json, LazyFrame.write_json、deserialize

## Block 5 — block_005.patch
定位：@@ -15,7 +20,2 @@
说明：if isinstance(file, StringIO):、file = BytesIO(file.getvalue().encode())、elif isinstance(file, (str, Path)):...
