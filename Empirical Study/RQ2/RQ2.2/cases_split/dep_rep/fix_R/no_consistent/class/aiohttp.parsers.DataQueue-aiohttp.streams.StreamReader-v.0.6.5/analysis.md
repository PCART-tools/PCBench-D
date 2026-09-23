# 一、突变情况分析

- **Total**: 59
- **替代API**: `aiohttp.streams.StreamReader`
- **10% 阈值**: 5.9

## Vi-1 (v.0.6.5-v0.9.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 2 | 0.3642 |
| tokenBased | 17 | 0.2792 |

## Vi (v0.7.0-v0.9.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 2 | 0.3929 |
| tokenBased | 10 | 0.3132 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 2 | 2 | +0 | false |
| tokenBased | 17 | 10 | +7 | true |

```json
{
  "total": 59,
  "replacement_api": "aiohttp.streams.StreamReader",
  "threshold_10pct": 5.9,
  "vi_minus_1": {
    "mapBased": {
      "rank": 2,
      "score": 0.364246
    },
    "tokenBased": {
      "rank": 17,
      "score": 0.279211
    }
  },
  "vi": {
    "mapBased": {
      "rank": 2,
      "score": 0.392932
    },
    "tokenBased": {
      "rank": 10,
      "score": 0.313162
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 2,
      "vi_rank": 2,
      "delta": 0,
      "exceeds_10pct": false
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 17,
      "vi_rank": 10,
      "delta": 7,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `aiohttp.parsers.DataQueue/Vi-1_v.0.6.5.py`
- **new**: `aiohttp.parsers.DataQueue/Vi_v0.7.0.py`
- **+17 / -9**

```diff
--- aiohttp.parsers.DataQueue/Vi-1_v.0.6.5.py
+++ aiohttp.parsers.DataQueue/Vi_v0.7.0.py
@@ -1,12 +1,16 @@
 class DataQueue:
     
 
-    def __init__(self, *, loop=None):
+    def __init__(self, stream, *, loop=None):
+        self._stream = stream
         self._loop = loop
         self._buffer = collections.deque()
         self._eof = False
         self._waiter = None
         self._exception = None
+
+    def at_eof(self):
+        return self._eof
 
     def exception(self):
         return self._exception
@@ -43,12 +47,16 @@
         if self._exception is not None:
             raise self._exception
 
-        if not self._buffer and not self._eof:
-            assert not self._waiter
-            self._waiter = asyncio.Future(loop=self._loop)
-            yield from self._waiter
+        self._stream.resume_stream()
+        try:
+            if not self._buffer and not self._eof:
+                assert not self._waiter
+                self._waiter = asyncio.Future(loop=self._loop)
+                yield from self._waiter
 
-        if self._buffer:
-            return self._buffer.popleft()
-        else:
-            raise EofStream
+            if self._buffer:
+                return self._buffer.popleft()
+            else:
+                raise EofStream
+        finally:
+            self._stream.pause_stream()
```

```json
{
  "old_file": "aiohttp.parsers.DataQueue/Vi-1_v.0.6.5.py",
  "new_file": "aiohttp.parsers.DataQueue/Vi_v0.7.0.py",
  "lines_added": 17,
  "lines_removed": 9
}
```
