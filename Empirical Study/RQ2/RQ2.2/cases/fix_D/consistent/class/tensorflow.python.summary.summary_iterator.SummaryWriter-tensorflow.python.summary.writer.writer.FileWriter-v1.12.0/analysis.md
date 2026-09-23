# 一、突变情况分析

- **Total**: 10
- **替代API**: `tensorflow.python.summary.writer.writer.FileWriter`
- **10% 阈值**: 1.0

## Vi-1 (0.12.1-v1.12.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 4 | 0.3086 |
| tokenBased | 6 | 0.2703 |

## Vi (0.12.1-v1.13.1)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 2 | 0.4009 |
| tokenBased | 4 | 0.3333 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 4 | 2 | +2 | true |
| tokenBased | 6 | 4 | +2 | true |

```json
{
  "total": 10,
  "replacement_api": "tensorflow.python.summary.writer.writer.FileWriter",
  "threshold_10pct": 1.0,
  "vi_minus_1": {
    "mapBased": {
      "rank": 4,
      "score": 0.308561
    },
    "tokenBased": {
      "rank": 6,
      "score": 0.270321
    }
  },
  "vi": {
    "mapBased": {
      "rank": 2,
      "score": 0.400876
    },
    "tokenBased": {
      "rank": 4,
      "score": 0.333333
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 4,
      "vi_rank": 2,
      "delta": 2,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 6,
      "vi_rank": 4,
      "delta": 2,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `R_candidates/Vi-1_v1.12.0/tensorflow.python.summary.writer.writer.FileWriter.py`
- **new**: `R_candidates/Vi_v1.13.1/tensorflow.python.summary.writer.writer.FileWriter.py`
- **+18 / -0**

```diff
--- R_candidates/Vi-1_v1.12.0/tensorflow.python.summary.writer.writer.FileWriter.py
+++ R_candidates/Vi_v1.13.1/tensorflow.python.summary.writer.writer.FileWriter.py
@@ -21,6 +21,8 @@
     else:
       event_writer = EventFileWriter(logdir, max_queue, flush_secs,
                                      filename_suffix)
+
+    self._closed = False
     super(FileWriter, self).__init__(event_writer, graph, graph_def)
 
   def __enter__(self):
@@ -35,18 +37,34 @@
     
     return self.event_writer.get_logdir()
 
+  def _warn_if_event_writer_is_closed(self):
+    if self._closed:
+      warnings.warn("Attempting to use a closed FileWriter. "
+                    "The operation will be a noop unless the FileWriter "
+                    "is explicitly reopened.")
+
+  def _add_event(self, event, step):
+    self._warn_if_event_writer_is_closed()
+    super(FileWriter, self)._add_event(event, step)
+
   def add_event(self, event):
     
+    self._warn_if_event_writer_is_closed()
     self.event_writer.add_event(event)
 
   def flush(self):
     
+
+
+    self._warn_if_event_writer_is_closed()
     self.event_writer.flush()
 
   def close(self):
     
     self.event_writer.close()
+    self._closed = True
 
   def reopen(self):
     
     self.event_writer.reopen()
+    self._closed = False
```

```json
{
  "old_file": "R_candidates/Vi-1_v1.12.0/tensorflow.python.summary.writer.writer.FileWriter.py",
  "new_file": "R_candidates/Vi_v1.13.1/tensorflow.python.summary.writer.writer.FileWriter.py",
  "lines_added": 18,
  "lines_removed": 0
}
```
