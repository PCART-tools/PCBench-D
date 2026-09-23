# 一、突变情况分析

- **Total**: 765
- **替代API**: `aiohttp.web_reqrep.StreamResponse.prepare`
- **10% 阈值**: 76.5

## Vi-1 (v0.17.4-v1.1.6)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 27 | 0.4257 |
| tokenBased | 140 | 0.3010 |
| treeBased | 102 | 0.4103 |

## Vi (v0.17.4-v1.2.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 40 | 0.4020 |
| tokenBased | 223 | 0.2330 |
| treeBased | 137 | 0.3851 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 27 | 40 | -13 | false |
| tokenBased | 140 | 223 | -83 | true |
| treeBased | 102 | 137 | -35 | false |

```json
{
  "total": 765,
  "replacement_api": "aiohttp.web_reqrep.StreamResponse.prepare",
  "threshold_10pct": 76.5,
  "vi_minus_1": {
    "mapBased": {
      "rank": 27,
      "score": 0.42572
    },
    "tokenBased": {
      "rank": 140,
      "score": 0.300971
    },
    "treeBased": {
      "rank": 102,
      "score": 0.410256
    }
  },
  "vi": {
    "mapBased": {
      "rank": 40,
      "score": 0.402017
    },
    "tokenBased": {
      "rank": 223,
      "score": 0.23301
    },
    "treeBased": {
      "rank": 137,
      "score": 0.385135
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 27,
      "vi_rank": 40,
      "delta": -13,
      "exceeds_10pct": false
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 140,
      "vi_rank": 223,
      "delta": -83,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 102,
      "vi_rank": 137,
      "delta": -35,
      "exceeds_10pct": false
    }
  ]
}
```

# 二、old → new Diff

- **old**: `R_candidates/Vi-1_v1.1.6/aiohttp.web_reqrep.StreamResponse.prepare.py`
- **new**: `R_candidates/Vi_v1.2.0/aiohttp.web_reqrep.StreamResponse.prepare.py`
- **+1 / -2**

```diff
--- R_candidates/Vi-1_v1.1.6/aiohttp.web_reqrep.StreamResponse.prepare.py
+++ R_candidates/Vi_v1.2.0/aiohttp.web_reqrep.StreamResponse.prepare.py
@@ -3,7 +3,6 @@
         resp_impl = self._start_pre_check(request)
         if resp_impl is not None:
             return resp_impl
-        for app in request.match_info.apps:
-            yield from app.on_response_prepare.send(request, self)
+        yield from request._prepare_hook(self)
 
         return self._start(request)
```

```json
{
  "old_file": "R_candidates/Vi-1_v1.1.6/aiohttp.web_reqrep.StreamResponse.prepare.py",
  "new_file": "R_candidates/Vi_v1.2.0/aiohttp.web_reqrep.StreamResponse.prepare.py",
  "lines_added": 1,
  "lines_removed": 2
}
```
