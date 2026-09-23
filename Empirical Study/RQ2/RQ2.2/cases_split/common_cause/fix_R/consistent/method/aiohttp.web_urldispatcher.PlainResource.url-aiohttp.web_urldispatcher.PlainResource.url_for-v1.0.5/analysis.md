# 一、突变情况分析

- **Total**: 971
- **替代API**: `aiohttp.web_urldispatcher.PlainResource.url_for`
- **10% 阈值**: 97.1

## Vi-1 (v1.0.5-v3.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 43 | 0.8571 |
| tokenBased | 3 | 0.5238 |
| treeBased | 31 | 0.7097 |

## Vi (v1.1.0-v3.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 49 | 0.7692 |
| tokenBased | 16 | 0.3871 |
| treeBased | 159 | 0.5526 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 43 | 49 | -6 | false |
| tokenBased | 3 | 16 | -13 | false |
| treeBased | 31 | 159 | -128 | true |

```json
{
  "total": 971,
  "replacement_api": "aiohttp.web_urldispatcher.PlainResource.url_for",
  "threshold_10pct": 97.1,
  "vi_minus_1": {
    "mapBased": {
      "rank": 43,
      "score": 0.857143
    },
    "tokenBased": {
      "rank": 3,
      "score": 0.52381
    },
    "treeBased": {
      "rank": 31,
      "score": 0.709677
    }
  },
  "vi": {
    "mapBased": {
      "rank": 49,
      "score": 0.769231
    },
    "tokenBased": {
      "rank": 16,
      "score": 0.387097
    },
    "treeBased": {
      "rank": 159,
      "score": 0.552632
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 43,
      "vi_rank": 49,
      "delta": -6,
      "exceeds_10pct": false
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 3,
      "vi_rank": 16,
      "delta": -13,
      "exceeds_10pct": false
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 31,
      "vi_rank": 159,
      "delta": -128,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `aiohttp.web_urldispatcher.PlainResource.url/Vi-1_v1.0.5.py`
- **new**: `aiohttp.web_urldispatcher.PlainResource.url/Vi_v1.1.0.py`
- **+2 / -1**

```diff
--- aiohttp.web_urldispatcher.PlainResource.url/Vi-1_v1.0.5.py
+++ aiohttp.web_urldispatcher.PlainResource.url/Vi_v1.1.0.py
@@ -1,2 +1,3 @@
     def url(self, *, query=None):
-        return self._append_query(self._path, query)
+        super().url()
+        return str(self.url_for().with_query(query))
```

```json
{
  "old_file": "aiohttp.web_urldispatcher.PlainResource.url/Vi-1_v1.0.5.py",
  "new_file": "aiohttp.web_urldispatcher.PlainResource.url/Vi_v1.1.0.py",
  "lines_added": 2,
  "lines_removed": 1
}
```
