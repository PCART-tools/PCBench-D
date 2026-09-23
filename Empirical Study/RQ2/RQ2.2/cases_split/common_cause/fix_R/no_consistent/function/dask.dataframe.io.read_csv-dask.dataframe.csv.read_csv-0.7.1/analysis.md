# 一、突变情况分析

- **Total**: 99
- **替代API**: `dask.dataframe.csv.read_csv`
- **10% 阈值**: 9.9

## Vi-1 (0.7.1-0.9.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 10 | 0.2966 |
| tokenBased | 5 | 0.4886 |
| treeBased | 2 | 0.4275 |

## Vi (0.7.2-0.9.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 21 | 0.2695 |
| tokenBased | 4 | 0.5323 |
| treeBased | 6 | 0.4129 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 10 | 21 | -11 | true |
| tokenBased | 5 | 4 | +1 | false |
| treeBased | 2 | 6 | -4 | false |

```json
{
  "total": 99,
  "replacement_api": "dask.dataframe.csv.read_csv",
  "threshold_10pct": 9.9,
  "vi_minus_1": {
    "mapBased": {
      "rank": 10,
      "score": 0.29662
    },
    "tokenBased": {
      "rank": 5,
      "score": 0.488571
    },
    "treeBased": {
      "rank": 2,
      "score": 0.427495
    }
  },
  "vi": {
    "mapBased": {
      "rank": 21,
      "score": 0.269525
    },
    "tokenBased": {
      "rank": 4,
      "score": 0.532258
    },
    "treeBased": {
      "rank": 6,
      "score": 0.412863
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 10,
      "vi_rank": 21,
      "delta": -11,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 5,
      "vi_rank": 4,
      "delta": 1,
      "exceeds_10pct": false
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 2,
      "vi_rank": 6,
      "delta": -4,
      "exceeds_10pct": false
    }
  ]
}
```

# 二、old → new Diff

- **old**: `dask.dataframe.io.read_csv/Vi-1_0.7.1.py`
- **new**: `dask.dataframe.io.read_csv/Vi_0.7.2.py`
- **+20 / -30**

```diff
--- dask.dataframe.io.read_csv/Vi-1_0.7.1.py
+++ dask.dataframe.io.read_csv/Vi_0.7.2.py
@@ -2,58 +2,48 @@
 
 @wraps(pd.read_csv)
 def read_csv(fn, *args, **kwargs):
+    if 'nrows' in kwargs:
+        df = read_csv(fn, *args, **dissoc(kwargs, 'nrows'))
+        return df.head(kwargs['nrows'], compute=False)
+
     chunkbytes = kwargs.pop('chunkbytes', 2**25)
-    categorize = kwargs.pop('categorize', None)
     index = kwargs.pop('index', None)
-    if index and categorize == None:
-        categorize = True
+    kwargs = kwargs.copy()
 
     kwargs = fill_kwargs(fn, args, kwargs)
 
 
     if '*' in fn:
+        from .multi import concat
         return concat([read_csv(f, *args, **kwargs) for f in sorted(glob(fn))])
 
     token = tokenize(os.path.getmtime(fn), args, kwargs)
     name = 'read-csv-%s-%s' % (fn, token)
+    bom = get_bom(fn)
 
     columns = kwargs.pop('columns')
     header = kwargs.pop('header')
 
-    if 'nrows' in kwargs:
-        dsk = {(name, 0): (apply, pd.read_csv, (fn,),
-                                  assoc(kwargs, 'header', header))}
-        result = DataFrame(dsk, name, columns, [None, None])
 
-    else:
+    total_bytes = file_size(fn, kwargs['compression'])
+    nchunks = int(ceil(total_bytes / chunkbytes))
+    divisions = [None] * (nchunks + 1)
 
-        total_bytes = file_size(fn, kwargs['compression'])
-        nchunks = int(ceil(total_bytes / chunkbytes))
-        divisions = [None] * (nchunks + 1)
-
-        first_kwargs = merge(kwargs, dict(header=header, compression=None))
-        rest_kwargs = merge(kwargs, dict(header=None, compression=None))
+    first_kwargs = merge(kwargs, dict(header=header, compression=None))
+    rest_kwargs = merge(kwargs, dict(header=None, compression=None))
 
 
-        dsk = dict(((name, i), (_read_csv, fn, i, chunkbytes,
-                                           kwargs['compression'], rest_kwargs))
-                   for i in range(1, nchunks))
+    dsk = dict(((name, i), (_read_csv, fn, i, chunkbytes,
+                                       kwargs['compression'], rest_kwargs,
+                                       bom))
+               for i in range(1, nchunks))
 
-        dsk[(name, 0)] = (_read_csv, fn, 0, chunkbytes, kwargs['compression'],
-                                     first_kwargs)
+    dsk[(name, 0)] = (_read_csv, fn, 0, chunkbytes, kwargs['compression'],
+                                 first_kwargs, b'')
 
-        result = DataFrame(dsk, name, columns, divisions)
-
-    if categorize or index:
-        categories, quantiles = categories_and_quantiles(fn, args, kwargs,
-                                                         index, categorize,
-                                                         chunkbytes=chunkbytes)
-
-    if categorize:
-        func = partial(categorize_block, categories=categories)
-        result = result.map_partitions(func, columns=columns)
+    result = DataFrame(dsk, name, columns, divisions)
 
     if index:
-        result = set_partition(result, index, quantiles)
+        result = result.set_index(index)
 
     return result
```

```json
{
  "old_file": "dask.dataframe.io.read_csv/Vi-1_0.7.1.py",
  "new_file": "dask.dataframe.io.read_csv/Vi_0.7.2.py",
  "lines_added": 20,
  "lines_removed": 30
}
```
