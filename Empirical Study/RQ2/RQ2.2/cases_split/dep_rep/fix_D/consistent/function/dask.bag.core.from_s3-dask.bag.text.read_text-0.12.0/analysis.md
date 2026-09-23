# 一、突变情况分析

- **Total**: 37
- **替代API**: `dask.bag.text.read_text`
- **10% 阈值**: 3.7

## Vi-1 (0.8.2-0.12.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 27 | 0.3166 |
| tokenBased | 21 | 0.3220 |
| treeBased | 27 | 0.3593 |

## Vi (0.8.2-0.13.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 19 | 0.3985 |
| tokenBased | 14 | 0.3882 |
| treeBased | 16 | 0.4157 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 27 | 19 | +8 | true |
| tokenBased | 21 | 14 | +7 | true |
| treeBased | 27 | 16 | +11 | true |

```json
{
  "total": 37,
  "replacement_api": "dask.bag.text.read_text",
  "threshold_10pct": 3.7,
  "vi_minus_1": {
    "mapBased": {
      "rank": 27,
      "score": 0.31665
    },
    "tokenBased": {
      "rank": 21,
      "score": 0.321951
    },
    "treeBased": {
      "rank": 27,
      "score": 0.359322
    }
  },
  "vi": {
    "mapBased": {
      "rank": 19,
      "score": 0.398518
    },
    "tokenBased": {
      "rank": 14,
      "score": 0.388235
    },
    "treeBased": {
      "rank": 16,
      "score": 0.415686
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 27,
      "vi_rank": 19,
      "delta": 8,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 21,
      "vi_rank": 14,
      "delta": 7,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 27,
      "vi_rank": 16,
      "delta": 11,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `R_candidates/Vi-1_0.12.0/dask.bag.text.read_text.py`
- **new**: `R_candidates/Vi_0.13.0/dask.bag.text.read_text.py`
- **+3 / -13**

```diff
--- R_candidates/Vi-1_0.12.0/dask.bag.text.read_text.py
+++ R_candidates/Vi_0.13.0/dask.bag.text.read_text.py
@@ -10,22 +10,12 @@
                       storage_options=storage_options)
                      for fn in urlpath], [])
     else:
-        if compression == 'infer':
-            compression = infer_compression(urlpath)
-
-        if blocksize and compression not in seekable_files:
-            msg = ("Compression %s does not support breaking apart files\n"
-                   "Use ``blocksize=None`` or decompress file externally")
-            raise ValueError(msg % compression)
-        if compression not in seekable_files and compression not in cfiles:
-            raise NotImplementedError("Compression format %s not installed" %
-                                      compression)
-
-        elif blocksize is None:
+        if blocksize is None:
             files = open_text_files(urlpath, encoding=encoding, errors=errors,
                                     compression=compression,
                                     **(storage_options or {}))
-            blocks = [delayed(list)(file) for file in files]
+            blocks = [delayed(list, pure=True)(delayed(file_to_blocks)(file))
+                      for file in files]
 
         else:
             _, blocks = read_bytes(urlpath, delimiter=linedelimiter.encode(),
```

```json
{
  "old_file": "R_candidates/Vi-1_0.12.0/dask.bag.text.read_text.py",
  "new_file": "R_candidates/Vi_0.13.0/dask.bag.text.read_text.py",
  "lines_added": 3,
  "lines_removed": 13
}
```
