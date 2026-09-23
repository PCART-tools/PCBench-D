# 一、突变情况分析

- **Total**: 813
- **替代API**: `aiohttp.web.Application.on_cleanup`
- **10% 阈值**: 81.3

## Vi-1 (v0.20.2-2.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 378 | 0.3442 |
| tokenBased | 89 | 0.2667 |
| treeBased | 267 | 0.5172 |

## Vi (v0.21.0-2.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 414 | 0.3149 |
| tokenBased | 346 | 0.2105 |
| treeBased | 524 | 0.3750 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 378 | 414 | -36 | false |
| tokenBased | 89 | 346 | -257 | true |
| treeBased | 267 | 524 | -257 | true |

```json
{
  "total": 813,
  "replacement_api": "aiohttp.web.Application.on_cleanup",
  "threshold_10pct": 81.3,
  "vi_minus_1": {
    "mapBased": {
      "rank": 378,
      "score": 0.344186
    },
    "tokenBased": {
      "rank": 89,
      "score": 0.266667
    },
    "treeBased": {
      "rank": 267,
      "score": 0.517241
    }
  },
  "vi": {
    "mapBased": {
      "rank": 414,
      "score": 0.314894
    },
    "tokenBased": {
      "rank": 346,
      "score": 0.210526
    },
    "treeBased": {
      "rank": 524,
      "score": 0.375
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 378,
      "vi_rank": 414,
      "delta": -36,
      "exceeds_10pct": false
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 89,
      "vi_rank": 346,
      "delta": -257,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 267,
      "vi_rank": 524,
      "delta": -257,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `aiohttp.web.Application.register_on_finish/Vi-1_v0.20.2.py`
- **new**: `aiohttp.web.Application.register_on_finish/Vi_v0.21.0.py`
- **+2 / -1**

```diff
--- aiohttp.web.Application.register_on_finish/Vi-1_v0.20.2.py
+++ aiohttp.web.Application.register_on_finish/Vi_v0.21.0.py
@@ -1,2 +1,3 @@
     def register_on_finish(self, func, *args, **kwargs):
-        self._finish_callbacks.insert(0, (func, args, kwargs))
+        warnings.warn("Use .on_cleanup.append() instead", DeprecationWarning)
+        self.on_cleanup.append(lambda app: func(app, *args, **kwargs))
```

```json
{
  "old_file": "aiohttp.web.Application.register_on_finish/Vi-1_v0.20.2.py",
  "new_file": "aiohttp.web.Application.register_on_finish/Vi_v0.21.0.py",
  "lines_added": 2,
  "lines_removed": 1
}
```
