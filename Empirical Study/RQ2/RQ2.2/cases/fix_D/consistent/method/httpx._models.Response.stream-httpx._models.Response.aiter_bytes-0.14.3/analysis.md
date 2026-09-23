# 一、突变情况分析

- **Total**: 330
- **替代API**: `httpx._models.Response.aiter_bytes`
- **10% 阈值**: 33.0

## Vi-1 (0.13.3-0.14.3)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 294 | 0.2252 |
| tokenBased | 206 | 0.1458 |
| treeBased | 215 | 0.3333 |

## Vi (0.13.3-0.15.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 257 | 0.2377 |
| tokenBased | 201 | 0.1321 |
| treeBased | 207 | 0.3016 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 294 | 257 | +37 | true |
| tokenBased | 206 | 201 | +5 | false |
| treeBased | 215 | 207 | +8 | false |

```json
{
  "total": 330,
  "replacement_api": "httpx._models.Response.aiter_bytes",
  "threshold_10pct": 33.0,
  "vi_minus_1": {
    "mapBased": {
      "rank": 294,
      "score": 0.22524
    },
    "tokenBased": {
      "rank": 206,
      "score": 0.145833
    },
    "treeBased": {
      "rank": 215,
      "score": 0.333333
    }
  },
  "vi": {
    "mapBased": {
      "rank": 257,
      "score": 0.237705
    },
    "tokenBased": {
      "rank": 201,
      "score": 0.132075
    },
    "treeBased": {
      "rank": 207,
      "score": 0.301587
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 294,
      "vi_rank": 257,
      "delta": 37,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 206,
      "vi_rank": 201,
      "delta": 5,
      "exceeds_10pct": false
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 215,
      "vi_rank": 207,
      "delta": 8,
      "exceeds_10pct": false
    }
  ]
}
```

# 二、old → new Diff

- **old**: `R_candidates/Vi-1_0.14.3/httpx._models.Response.aiter_bytes.py`
- **new**: `R_candidates/Vi_0.15.0/httpx._models.Response.aiter_bytes.py`
- **+3 / -2**

```diff
--- R_candidates/Vi-1_0.14.3/httpx._models.Response.aiter_bytes.py
+++ R_candidates/Vi_0.15.0/httpx._models.Response.aiter_bytes.py
@@ -3,7 +3,8 @@
         if hasattr(self, "_content"):
             yield self._content
         else:
+            decoder = self._get_content_decoder()
             with self._wrap_decoder_errors():
                 async for chunk in self.aiter_raw():
-                    yield self.decoder.decode(chunk)
-                yield self.decoder.flush()
+                    yield decoder.decode(chunk)
+                yield decoder.flush()
```

```json
{
  "old_file": "R_candidates/Vi-1_0.14.3/httpx._models.Response.aiter_bytes.py",
  "new_file": "R_candidates/Vi_0.15.0/httpx._models.Response.aiter_bytes.py",
  "lines_added": 3,
  "lines_removed": 2
}
```
