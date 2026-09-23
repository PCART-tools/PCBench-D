# 一、突变情况分析

- **Total**: 580
- **替代API**: `numpy.lib.npyio.genfromtxt`
- **10% 阈值**: 58.0

## Vi-1 (v1.21.5-v1.22.4)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 580 | 0.0215 |
| tokenBased | 580 | 0.0110 |
| treeBased | 580 | 0.0193 |

## Vi (v1.21.5-v1.23.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 652 | 0.0214 |
| tokenBased | 652 | 0.0109 |
| treeBased | 652 | 0.0192 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 580 | 652 | -72 | true |
| tokenBased | 580 | 652 | -72 | true |
| treeBased | 580 | 652 | -72 | true |

```json
{
  "total": 580,
  "replacement_api": "numpy.lib.npyio.genfromtxt",
  "threshold_10pct": 58.0,
  "vi_minus_1": {
    "mapBased": {
      "rank": 580,
      "score": 0.021464
    },
    "tokenBased": {
      "rank": 580,
      "score": 0.010972
    },
    "treeBased": {
      "rank": 580,
      "score": 0.019308
    }
  },
  "vi": {
    "mapBased": {
      "rank": 652,
      "score": 0.021352
    },
    "tokenBased": {
      "rank": 652,
      "score": 0.010932
    },
    "treeBased": {
      "rank": 652,
      "score": 0.019222
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 580,
      "vi_rank": 652,
      "delta": -72,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 580,
      "vi_rank": 652,
      "delta": -72,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 580,
      "vi_rank": 652,
      "delta": -72,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `R_candidates/Vi-1_v1.22.4/numpy.lib.npyio.genfromtxt.py`
- **new**: `R_candidates/Vi_v1.23.0/numpy.lib.npyio.genfromtxt.py`
- **+18 / -14**

```diff
--- R_candidates/Vi-1_v1.22.4/numpy.lib.npyio.genfromtxt.py
+++ R_candidates/Vi_v1.23.0/numpy.lib.npyio.genfromtxt.py
@@ -7,8 +7,8 @@
                deletechars=''.join(sorted(NameValidator.defaultdeletechars)),
                replace_space='_', autostrip=False, case_sensitive=True,
                defaultfmt="f%i", unpack=None, usemask=False, loose=True,
-               invalid_raise=True, max_rows=None, encoding='bytes', *,
-               like=None):
+               invalid_raise=True, max_rows=None, encoding='bytes',
+               *, ndmin=0, like=None):
     
 
     if like is not None:
@@ -22,8 +22,11 @@
             case_sensitive=case_sensitive, defaultfmt=defaultfmt,
             unpack=unpack, usemask=usemask, loose=loose,
             invalid_raise=invalid_raise, max_rows=max_rows, encoding=encoding,
+            ndmin=ndmin,
             like=like
         )
+
+    _ensure_ndmin_ndarray_check_param(ndmin)
 
     if max_rows is not None:
         if skip_footer:
@@ -49,22 +52,21 @@
         byte_converters = False
 
 
+    if isinstance(fname, os_PathLike):
+        fname = os_fspath(fname)
+    if isinstance(fname, str):
+        fid = np.lib._datasource.open(fname, 'rt', encoding=encoding)
+        fid_ctx = contextlib.closing(fid)
+    else:
+        fid = fname
+        fid_ctx = contextlib.nullcontext(fid)
     try:
-        if isinstance(fname, os_PathLike):
-            fname = os_fspath(fname)
-        if isinstance(fname, str):
-            fid = np.lib._datasource.open(fname, 'rt', encoding=encoding)
-            fid_ctx = contextlib.closing(fid)
-        else:
-            fid = fname
-            fid_ctx = contextlib.nullcontext(fid)
         fhd = iter(fid)
     except TypeError as e:
         raise TypeError(
-            f"fname must be a string, filehandle, list of strings,\n"
-            f"or generator. Got {type(fname)} instead."
+            "fname must be a string, a filehandle, a sequence of strings,\n"
+            f"or an iterator of strings. Got {type(fname)} instead."
         ) from e
-
     with fid_ctx:
         split_line = LineSplitter(delimiter=delimiter, comments=comments,
                                   autostrip=autostrip, encoding=encoding)
@@ -534,7 +536,9 @@
     if usemask:
         output = output.view(MaskedArray)
         output._mask = outputmask
-    output = np.squeeze(output)
+
+    output = _ensure_ndmin_ndarray(output, ndmin=ndmin)
+
     if unpack:
         if names is None:
             return output.T
```

```json
{
  "old_file": "R_candidates/Vi-1_v1.22.4/numpy.lib.npyio.genfromtxt.py",
  "new_file": "R_candidates/Vi_v1.23.0/numpy.lib.npyio.genfromtxt.py",
  "lines_added": 18,
  "lines_removed": 14
}
```
