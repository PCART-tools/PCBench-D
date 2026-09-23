# 一、突变情况分析

- **Total**: 972
- **替代API**: `dask.delayed.delayed`
- **10% 阈值**: 97.2

## Vi-1 (0.8.2-0.11.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 5 | 0.6921 |
| tokenBased | 1 | 0.6316 |
| treeBased | 1 | 0.7120 |

## Vi (0.8.2-0.11.1)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 201 | 0.4675 |
| tokenBased | 217 | 0.3684 |
| treeBased | 107 | 0.4734 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 5 | 201 | -196 | true |
| tokenBased | 1 | 217 | -216 | true |
| treeBased | 1 | 107 | -106 | true |

```json
{
  "total": 972,
  "replacement_api": "dask.delayed.delayed",
  "threshold_10pct": 97.2,
  "vi_minus_1": {
    "mapBased": {
      "rank": 5,
      "score": 0.692133
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.631579
    },
    "treeBased": {
      "rank": 1,
      "score": 0.712
    }
  },
  "vi": {
    "mapBased": {
      "rank": 201,
      "score": 0.467523
    },
    "tokenBased": {
      "rank": 217,
      "score": 0.368421
    },
    "treeBased": {
      "rank": 107,
      "score": 0.473404
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 5,
      "vi_rank": 201,
      "delta": -196,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 1,
      "vi_rank": 217,
      "delta": -216,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 1,
      "vi_rank": 107,
      "delta": -106,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `R_candidates/Vi-1_0.11.0/dask.delayed.delayed.py`
- **new**: `R_candidates/Vi_0.11.1/dask.delayed.delayed.py`
- **+12 / -2**

```diff
--- R_candidates/Vi-1_0.11.0/dask.delayed.delayed.py
+++ R_candidates/Vi_0.11.1/dask.delayed.delayed.py
@@ -1,5 +1,5 @@
 @curry
-def delayed(obj, name=None, pure=False):
+def delayed(obj, name=None, pure=False, nout=None):
     
     if isinstance(obj, Delayed):
         return obj
@@ -7,7 +7,17 @@
     task, dasks = to_task_dasks(obj)
 
     if not dasks:
-        return DelayedLeaf(obj, pure=pure, name=name)
+        if not (nout is None or (type(nout) is int and nout >= 0)):
+            raise ValueError("nout must be None or a positive integer,"
+                             " got %s" % nout)
+        if not name:
+            try:
+                prefix = obj.__name__
+            except AttributeError:
+                prefix = type(obj).__name__
+            token = tokenize(obj, nout, pure=pure)
+            name = '%s-%s' % (prefix, token)
+        return DelayedLeaf(obj, name, pure=pure, nout=nout)
     else:
         if not name:
             name = '%s-%s' % (type(obj).__name__, tokenize(task, pure=pure))
```

```json
{
  "old_file": "R_candidates/Vi-1_0.11.0/dask.delayed.delayed.py",
  "new_file": "R_candidates/Vi_0.11.1/dask.delayed.delayed.py",
  "lines_added": 12,
  "lines_removed": 2
}
```
