# Diff 分块分析：dask.dataframe.io.read_csv-dask.dataframe.csv.read_csv-0.7.1
## 文件定位

- 旧文件：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/no_consistent/function/dask.dataframe.io.read_csv-dask.dataframe.csv.read_csv-0.7.1/dask.dataframe.io.read_csv/Vi-1_0.7.1.py
- 新文件：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/no_consistent/function/dask.dataframe.io.read_csv-dask.dataframe.csv.read_csv-0.7.1/dask.dataframe.io.read_csv/Vi_0.7.2.py
- 目标文件（Target）：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/no_consistent/function/dask.dataframe.io.read_csv-dask.dataframe.csv.read_csv-0.7.1/R_candidates/0.9.0/dask.dataframe.csv.read_csv.py
- 实验组：fix_R
- 总变更：+22 / -32 行
- 分块数：7

## Block 1 — block_001.patch
定位：@@ -4,2 +4,6 @@
说明：if 'nrows' in kwargs:  # Just create single partition、df = read_csv(fn, *args, **dissoc(kwargs, 'nrows'))、return df.head(kwargs['nrows'], compute=False)...

## Block 2 — block_002.patch
定位：@@ -5,3 +9,2 @@
说明：categorize = kwargs.pop('categorize', None)

## Block 3 — block_003.patch
定位：@@ -7,4 +10,3 @@
说明：if index and categorize == None:、categorize = True、kwargs = kwargs.copy()

## Block 4 — block_004.patch
定位：@@ -14,2 +16,3 @@
说明：from .multi import concat

## Block 5 — block_005.patch
定位：@@ -18,2 +21,3 @@
说明：bom = get_bom(fn)

## Block 6 — block_006.patch
定位：@@ -22,6 +26,6 @@ / @@ -27,7 +31,4 @@ / @@ -33,4 +34,7 @@ / @@ -36,6 +40,4 @@ / @@ -41,15 +43,3 @@
说明：if 'nrows' in kwargs:  # Just create single partition、dsk = {(name, 0): (apply, pd.read_csv, (fn,),、assoc(kwargs, 'header', header))}... / else:、# Chunk sizes and numbers、total_bytes = file_size(fn, kwargs['compression'])... / first_kwargs = merge(kwargs, dict(header=header, compression、rest_kwargs = merge(kwargs, dict(header=None, compression=No、# Create dask graph... / # Create dask graph、dsk = dict(((name, i), (_read_csv, fn, i, chunkbytes,、kwargs['compression'], rest_kwargs))... / dsk[(name, 0)] = (_read_csv, fn, 0, chunkbytes, kwargs['comp、first_kwargs)、...
## Block 7 — block_007.patch
定位：@@ -56,3 +46,3 @@
说明：result = set_partition(result, index, quantiles)、result = result.set_index(index)
