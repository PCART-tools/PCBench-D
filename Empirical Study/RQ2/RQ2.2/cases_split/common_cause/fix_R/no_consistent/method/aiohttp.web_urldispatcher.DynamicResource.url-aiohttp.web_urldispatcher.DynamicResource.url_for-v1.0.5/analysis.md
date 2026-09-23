# 一、突变情况分析

- **Total**: 971
- **替代API**: `aiohttp.web_urldispatcher.DynamicResource.url_for`
- **10% 阈值**: 97.1

## Vi-1 (v1.0.5-v3.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 1 | 0.9027 |
| tokenBased | 34 | 0.4500 |
| treeBased | 124 | 0.5517 |

## Vi (v1.1.0-v3.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 84 | 0.7234 |
| tokenBased | 7 | 0.4545 |
| treeBased | 255 | 0.4762 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 1 | 84 | -83 | false |
| tokenBased | 34 | 7 | +27 | false |
| treeBased | 124 | 255 | -131 | true |

```json
{
  "total": 971,
  "replacement_api": "aiohttp.web_urldispatcher.DynamicResource.url_for",
  "threshold_10pct": 97.1,
  "vi_minus_1": {
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
  "vi": {
    "mapBased": {
      "rank": 84,
      "score": 0.723448
    },
    "tokenBased": {
      "rank": 7,
      "score": 0.454545
    },
    "treeBased": {
      "rank": 255,
      "score": 0.47619
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 1,
      "vi_rank": 84,
      "delta": -83,
      "exceeds_10pct": false
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 34,
      "vi_rank": 7,
      "delta": 27,
      "exceeds_10pct": false
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 124,
      "vi_rank": 255,
      "delta": -131,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `aiohttp.web_urldispatcher.DynamicResource.url/Vi-1_v1.0.5.py`
- **new**: `aiohttp.web_urldispatcher.DynamicResource.url/Vi_v1.1.0.py`
- **+2 / -2**

```diff
--- aiohttp.web_urldispatcher.DynamicResource.url/Vi-1_v1.0.5.py
+++ aiohttp.web_urldispatcher.DynamicResource.url/Vi_v1.1.0.py
@@ -1,3 +1,3 @@
     def url(self, *, parts, query=None):
-        url = self._formatter.format_map(parts)
-        return self._append_query(url, query)
+        super().url(**parts)
+        return str(self.url_for(**parts).with_query(query))
```

```json
{
  "old_file": "aiohttp.web_urldispatcher.DynamicResource.url/Vi-1_v1.0.5.py",
  "new_file": "aiohttp.web_urldispatcher.DynamicResource.url/Vi_v1.1.0.py",
  "lines_added": 2,
  "lines_removed": 2
}
```
