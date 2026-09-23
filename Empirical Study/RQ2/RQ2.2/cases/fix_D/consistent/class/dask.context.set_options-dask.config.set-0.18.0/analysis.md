# 一、突变情况分析

- **Total**: 112
- **替代API**: `dask.config.set`
- **10% 阈值**: 11.2

## Vi-1 (0.17.5-0.18.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 1 | 0.6186 |
| tokenBased | 5 | 0.4060 |

## Vi (0.17.5-0.18.1)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 2 | 0.4188 |
| tokenBased | 56 | 0.2082 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 1 | 2 | -1 | false |
| tokenBased | 5 | 56 | -51 | true |

```json
{
  "total": 112,
  "replacement_api": "dask.config.set",
  "threshold_10pct": 11.2,
  "vi_minus_1": {
    "mapBased": {
      "rank": 1,
      "score": 0.61862
    },
    "tokenBased": {
      "rank": 5,
      "score": 0.406015
    }
  },
  "vi": {
    "mapBased": {
      "rank": 2,
      "score": 0.418817
    },
    "tokenBased": {
      "rank": 56,
      "score": 0.208163
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 1,
      "vi_rank": 2,
      "delta": -1,
      "exceeds_10pct": false
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 5,
      "vi_rank": 56,
      "delta": -51,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `R_candidates/Vi-1_0.18.0/dask.config.set.py`
- **new**: `R_candidates/Vi_0.18.1/dask.config.set.py`
- **+35 / -14**

```diff
--- R_candidates/Vi-1_0.18.0/dask.config.set.py
+++ R_candidates/Vi_0.18.1/dask.config.set.py
@@ -6,23 +6,44 @@
 
         with lock:
             self.config = config
-            self.old = copy.deepcopy(config)
-
-            def assign(keys, value, d):
-                key = keys[0]
-                if len(keys) == 1:
-                    d[keys[0]] = value
-                else:
-                    if key not in d:
-                        d[key] = {}
-                    assign(keys[1:], value, d[key])
+            self.old = {}
 
             for key, value in kwargs.items():
-                assign(key.split('.'), value, config)
+                self._assign(key.split('.'), value, config, old=self.old)
 
     def __enter__(self):
-        return config
+        return self.config
 
     def __exit__(self, type, value, traceback):
-        self.config.clear()
-        self.config.update(self.old)
+        for keys, value in self.old.items():
+            if value == '--delete--':
+                d = self.config
+                try:
+                    while len(keys) > 1:
+                        d = d[keys[0]]
+                        keys = keys[1:]
+                    del d[keys[0]]
+                except KeyError:
+                    pass
+            else:
+                self._assign(keys, value, self.config)
+
+    @classmethod
+    def _assign(cls, keys, value, d, old=None, path=[]):
+        
+        if len(keys) == 1:
+            if old is not None:
+                path_key = tuple(path + [keys[0]])
+                if keys[0] in d:
+                    old[path_key] = d[keys[0]]
+                else:
+                    old[path_key] = '--delete--'
+            d[keys[0]] = value
+        else:
+            key = keys[0]
+            if key not in d:
+                d[key] = {}
+                if old is not None:
+                    old[tuple(path + [key])] = '--delete--'
+                old = None
+            cls._assign(keys[1:], value, d[key], path=path + [key], old=old)
```

```json
{
  "old_file": "R_candidates/Vi-1_0.18.0/dask.config.set.py",
  "new_file": "R_candidates/Vi_0.18.1/dask.config.set.py",
  "lines_added": 35,
  "lines_removed": 14
}
```
