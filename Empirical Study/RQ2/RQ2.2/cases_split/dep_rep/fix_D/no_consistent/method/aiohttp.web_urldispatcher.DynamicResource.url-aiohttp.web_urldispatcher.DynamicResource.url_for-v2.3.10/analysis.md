# 一、突变情况分析

- **Total**: 963
- **替代API**: `aiohttp.web_urldispatcher.DynamicResource.url_for`
- **10% 阈值**: 96.3

## Vi-1 (v1.0.5-v2.3.10)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 1 | 0.9027 |
| tokenBased | 1 | 0.6429 |
| treeBased | 2 | 0.7381 |

## Vi (v1.0.5-v3.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 1 | 0.9027 |
| tokenBased | 34 | 0.4500 |
| treeBased | 124 | 0.5517 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 1 | 1 | +0 | false |
| tokenBased | 1 | 34 | -33 | false |
| treeBased | 2 | 124 | -122 | true |

```json
{
  "total": 963,
  "replacement_api": "aiohttp.web_urldispatcher.DynamicResource.url_for",
  "threshold_10pct": 96.3,
  "vi_minus_1": {
    "mapBased": {
      "rank": 1,
      "score": 0.902655
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.642857
    },
    "treeBased": {
      "rank": 2,
      "score": 0.738095
    }
  },
  "vi": {
    "mapBased": {
      "rank": 1,
      "score": 0.902655
    },
    "tokenBased": {
      "rank": 34,
      "score": 0.45
    },
    "treeBased": {
      "rank": 124,
      "score": 0.551724
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 1,
      "vi_rank": 1,
      "delta": 0,
      "exceeds_10pct": false
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 1,
      "vi_rank": 34,
      "delta": -33,
      "exceeds_10pct": false
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 2,
      "vi_rank": 124,
      "delta": -122,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `R_candidates/Vi-1_v2.3.10/aiohttp.web_urldispatcher.DynamicResource.url_for.py`
- **new**: `R_candidates/Vi_v3.0.0/aiohttp.web_urldispatcher.DynamicResource.url_for.py`
- **+3 / -2**

```diff
--- R_candidates/Vi-1_v2.3.10/aiohttp.web_urldispatcher.DynamicResource.url_for.py
+++ R_candidates/Vi_v3.0.0/aiohttp.web_urldispatcher.DynamicResource.url_for.py
@@ -1,3 +1,4 @@
     def url_for(self, **parts):
-        url = self._formatter.format_map(parts)
-        return URL(url)
+        url = self._formatter.format_map({k: URL.build(path=v).raw_path
+                                          for k, v in parts.items()})
+        return URL.build(path=url)
```

```json
{
  "old_file": "R_candidates/Vi-1_v2.3.10/aiohttp.web_urldispatcher.DynamicResource.url_for.py",
  "new_file": "R_candidates/Vi_v3.0.0/aiohttp.web_urldispatcher.DynamicResource.url_for.py",
  "lines_added": 3,
  "lines_removed": 2
}
```
