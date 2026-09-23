# 一、突变情况分析

- **Total**: 166
- **替代API**: `sklearn.datasets.lfw.fetch_lfw_pairs`
- **10% 阈值**: 16.6

## Vi-1 (0.16.1-0.19.2)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 43 | 0.2735 |
| tokenBased | 76 | 0.1103 |
| treeBased | 113 | 0.1543 |

## Vi (0.16.1-0.20.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 105 | 0.2034 |
| tokenBased | 125 | 0.0870 |
| treeBased | 169 | 0.1238 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 43 | 105 | -62 | true |
| tokenBased | 76 | 125 | -49 | true |
| treeBased | 113 | 169 | -56 | true |

```json
{
  "total": 166,
  "replacement_api": "sklearn.datasets.lfw.fetch_lfw_pairs",
  "threshold_10pct": 16.6,
  "vi_minus_1": {
    "mapBased": {
      "rank": 43,
      "score": 0.273526
    },
    "tokenBased": {
      "rank": 76,
      "score": 0.110345
    },
    "treeBased": {
      "rank": 113,
      "score": 0.154321
    }
  },
  "vi": {
    "mapBased": {
      "rank": 105,
      "score": 0.203424
    },
    "tokenBased": {
      "rank": 125,
      "score": 0.086957
    },
    "treeBased": {
      "rank": 169,
      "score": 0.123762
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 43,
      "vi_rank": 105,
      "delta": -62,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 76,
      "vi_rank": 125,
      "delta": -49,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 113,
      "vi_rank": 169,
      "delta": -56,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `R_candidates/Vi-1_0.19.2/sklearn.datasets.lfw.fetch_lfw_pairs.py`
- **new**: `R_candidates/Vi_0.20.0/sklearn.datasets.lfw.fetch_lfw_pairs.py`
- **+11 / -3**

```diff
--- R_candidates/Vi-1_0.19.2/sklearn.datasets.lfw.fetch_lfw_pairs.py
+++ R_candidates/Vi_0.20.0/sklearn.datasets.lfw.fetch_lfw_pairs.py
@@ -2,14 +2,18 @@
                     color=False, slice_=(slice(70, 195), slice(78, 172)),
                     download_if_missing=True):
     
-    lfw_home, data_folder_path = check_fetch_lfw(
+    lfw_home, data_folder_path = _check_fetch_lfw(
         data_home=data_home, funneled=funneled,
         download_if_missing=download_if_missing)
     logger.debug('Loading %s LFW pairs from %s', subset, lfw_home)
 
 
 
-    m = Memory(cachedir=lfw_home, compress=6, verbose=0)
+    if LooseVersion(joblib_version) < LooseVersion('0.12'):
+
+        m = Memory(cachedir=lfw_home, compress=6, verbose=0)
+    else:
+        m = Memory(location=lfw_home, compress=6, verbose=0)
     load_func = m.cache(_fetch_lfw_pairs)
 
 
@@ -28,7 +32,11 @@
         index_file_path, data_folder_path, resize=resize, color=color,
         slice_=slice_)
 
+    module_path = dirname(__file__)
+    with open(join(module_path, 'descr', 'lfw.rst')) as rst_file:
+        fdescr = rst_file.read()
+
 
     return Bunch(data=pairs.reshape(len(pairs), -1), pairs=pairs,
                  target=target, target_names=target_names,
-                 DESCR="'%s' segment of the LFW pairs dataset" % subset)
+                 DESCR=fdescr)
```

```json
{
  "old_file": "R_candidates/Vi-1_0.19.2/sklearn.datasets.lfw.fetch_lfw_pairs.py",
  "new_file": "R_candidates/Vi_0.20.0/sklearn.datasets.lfw.fetch_lfw_pairs.py",
  "lines_added": 11,
  "lines_removed": 3
}
```
