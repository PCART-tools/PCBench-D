# 一、突变情况分析

- **Total**: 52
- **替代API**: `aiohttp.connector.UnixConnector`
- **10% 阈值**: 5.2

## Vi-1 (v0.7.0-v0.8.1)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 15 | 0.1883 |
| tokenBased | 31 | 0.1792 |

## Vi (v0.7.0-0.8.2)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 6 | 0.2301 |
| tokenBased | 30 | 0.1979 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 15 | 6 | +9 | true |
| tokenBased | 31 | 30 | +1 | false |

```json
{
  "total": 52,
  "replacement_api": "aiohttp.connector.UnixConnector",
  "threshold_10pct": 5.2,
  "vi_minus_1": {
    "mapBased": {
      "rank": 15,
      "score": 0.188336
    },
    "tokenBased": {
      "rank": 31,
      "score": 0.179211
    }
  },
  "vi": {
    "mapBased": {
      "rank": 6,
      "score": 0.230137
    },
    "tokenBased": {
      "rank": 30,
      "score": 0.19788
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 15,
      "vi_rank": 6,
      "delta": 9,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 31,
      "vi_rank": 30,
      "delta": 1,
      "exceeds_10pct": false
    }
  ]
}
```

# 二、old → new Diff

- **old**: `R_candidates/Vi-1_v0.8.1/aiohttp.connector.UnixConnector.py`
- **new**: `R_candidates/Vi_0.8.2/aiohttp.connector.UnixConnector.py`
- **+7 / -2**

```diff
--- R_candidates/Vi-1_v0.8.1/aiohttp.connector.UnixConnector.py
+++ R_candidates/Vi_0.8.2/aiohttp.connector.UnixConnector.py
@@ -3,9 +3,14 @@
     def __init__(self, path, *args, **kw):
         super().__init__(*args, **kw)
 
-        self.path = path
+        self._path = path
+
+    @property
+    def path(self):
+        
+        return self._path
 
     @asyncio.coroutine
     def _create_connection(self, req, **kwargs):
         return (yield from self._loop.create_unix_connection(
-            self._factory, self.path, **kwargs))
+            self._factory, self._path, **kwargs))
```

```json
{
  "old_file": "R_candidates/Vi-1_v0.8.1/aiohttp.connector.UnixConnector.py",
  "new_file": "R_candidates/Vi_0.8.2/aiohttp.connector.UnixConnector.py",
  "lines_added": 7,
  "lines_removed": 2
}
```
