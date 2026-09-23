# 一、突变情况分析

- **Total**: 813
- **替代API**: `aiohttp.web.Application.on_cleanup`
- **10% 阈值**: 81.3

## Vi-1 (v0.20.2-2.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 587 | 0.1947 |
| tokenBased | 750 | 0.0781 |
| treeBased | 664 | 0.2051 |

## Vi (v0.21.0-2.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 241 | 0.4253 |
| tokenBased | 535 | 0.2000 |
| treeBased | 174 | 0.5517 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 587 | 241 | +346 | true |
| tokenBased | 750 | 535 | +215 | true |
| treeBased | 664 | 174 | +490 | true |

```json
{
  "total": 813,
  "replacement_api": "aiohttp.web.Application.on_cleanup",
  "threshold_10pct": 81.3,
  "vi_minus_1": {
    "mapBased": {
      "rank": 587,
      "score": 0.194737
    },
    "tokenBased": {
      "rank": 750,
      "score": 0.078125
    },
    "treeBased": {
      "rank": 664,
      "score": 0.205128
    }
  },
  "vi": {
    "mapBased": {
      "rank": 241,
      "score": 0.425287
    },
    "tokenBased": {
      "rank": 535,
      "score": 0.2
    },
    "treeBased": {
      "rank": 174,
      "score": 0.551724
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 587,
      "vi_rank": 241,
      "delta": 346,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 750,
      "vi_rank": 535,
      "delta": 215,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 664,
      "vi_rank": 174,
      "delta": 490,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `aiohttp.web.Application.finish/Vi-1_v0.20.2.py`
- **new**: `aiohttp.web.Application.finish/Vi_v0.21.0.py`
- **+3 / -15**

```diff
--- aiohttp.web.Application.finish/Vi-1_v0.20.2.py
+++ aiohttp.web.Application.finish/Vi_v0.21.0.py
@@ -1,17 +1,5 @@
     @asyncio.coroutine
     def finish(self):
-        callbacks = self._finish_callbacks
-        self._finish_callbacks = []
-
-        for (cb, args, kwargs) in callbacks:
-            try:
-                res = cb(self, *args, **kwargs)
-                if (asyncio.iscoroutine(res) or
-                        isinstance(res, asyncio.Future)):
-                    yield from res
-            except Exception as exc:
-                self._loop.call_exception_handler({
-                    'message': "Error in finish callback",
-                    'exception': exc,
-                    'application': self,
-                })
+        
+        warnings.warn("Use .cleanup() instead", DeprecationWarning)
+        yield from self.cleanup()
```

```json
{
  "old_file": "aiohttp.web.Application.finish/Vi-1_v0.20.2.py",
  "new_file": "aiohttp.web.Application.finish/Vi_v0.21.0.py",
  "lines_added": 3,
  "lines_removed": 15
}
```
