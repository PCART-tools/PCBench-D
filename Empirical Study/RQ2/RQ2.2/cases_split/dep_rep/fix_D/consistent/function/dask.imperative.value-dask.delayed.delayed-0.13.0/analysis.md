# 一、突变情况分析

- **Total**: 1086
- **替代API**: `dask.delayed.delayed`
- **10% 阈值**: 108.6

## Vi-1 (0.8.2-0.13.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 221 | 0.4675 |
| tokenBased | 227 | 0.3684 |
| treeBased | 101 | 0.4734 |

## Vi (0.8.2-0.14.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 622 | 0.3341 |
| tokenBased | 492 | 0.2919 |
| treeBased | 458 | 0.4000 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 221 | 622 | -401 | true |
| tokenBased | 227 | 492 | -265 | true |
| treeBased | 101 | 458 | -357 | true |

```json
{
  "total": 1086,
  "replacement_api": "dask.delayed.delayed",
  "threshold_10pct": 108.6,
  "vi_minus_1": {
    "mapBased": {
      "rank": 221,
      "score": 0.467523
    },
    "tokenBased": {
      "rank": 227,
      "score": 0.368421
    },
    "treeBased": {
      "rank": 101,
      "score": 0.473404
    }
  },
  "vi": {
    "mapBased": {
      "rank": 622,
      "score": 0.334115
    },
    "tokenBased": {
      "rank": 492,
      "score": 0.291925
    },
    "treeBased": {
      "rank": 458,
      "score": 0.4
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 221,
      "vi_rank": 622,
      "delta": -401,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 227,
      "vi_rank": 492,
      "delta": -265,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 101,
      "vi_rank": 458,
      "delta": -357,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `R_candidates/Vi-1_0.13.0/dask.delayed.delayed.py`
- **new**: `R_candidates/Vi_0.14.0/dask.delayed.delayed.py`
- **+9 / -5**

```diff
--- R_candidates/Vi-1_0.13.0/dask.delayed.delayed.py
+++ R_candidates/Vi_0.14.0/dask.delayed.delayed.py
@@ -1,12 +1,16 @@
 @curry
-def delayed(obj, name=None, pure=False, nout=None):
+def delayed(obj, name=None, pure=False, nout=None, traverse=True):
     
     if isinstance(obj, Delayed):
         return obj
 
-    task, dasks = to_task_dasks(obj)
+    if isinstance(obj, base.Base) or traverse:
+        task, dsk = to_task_dask(obj)
+    else:
+        task = quote(obj)
+        dsk = {}
 
-    if not dasks:
+    if task is obj:
         if not (nout is None or (type(nout) is int and nout >= 0)):
             raise ValueError("nout must be None or a positive integer,"
                              " got %s" % nout)
@@ -21,5 +25,5 @@
     else:
         if not name:
             name = '%s-%s' % (type(obj).__name__, tokenize(task, pure=pure))
-        dasks.append({name: task})
-        return Delayed(name, dasks)
+        dsk = sharedict.merge(dsk, (name, {name: task}))
+        return Delayed(name, dsk)
```

```json
{
  "old_file": "R_candidates/Vi-1_0.13.0/dask.delayed.delayed.py",
  "new_file": "R_candidates/Vi_0.14.0/dask.delayed.delayed.py",
  "lines_added": 9,
  "lines_removed": 5
}
```
