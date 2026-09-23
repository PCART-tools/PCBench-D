# 一、突变情况分析

- **Total**: 971
- **替代API**: `aiohttp.web_urldispatcher.AbstractRoute.url_for`
- **10% 阈值**: 97.1

## Vi-1 (v1.0.5-v3.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 15 | 0.8931 |
| tokenBased | 2 | 0.6923 |
| treeBased | 7 | 0.8421 |

## Vi (v1.1.0-v3.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 19 | 0.7933 |
| tokenBased | 7 | 0.4500 |
| treeBased | 117 | 0.5926 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 15 | 19 | -4 | false |
| tokenBased | 2 | 7 | -5 | false |
| treeBased | 7 | 117 | -110 | true |

```json
{
  "total": 971,
  "replacement_api": "aiohttp.web_urldispatcher.AbstractRoute.url_for",
  "threshold_10pct": 97.1,
  "vi_minus_1": {
    "mapBased": {
      "rank": 15,
      "score": 0.893082
    },
    "tokenBased": {
      "rank": 2,
      "score": 0.692308
    },
    "treeBased": {
      "rank": 7,
      "score": 0.842105
    }
  },
  "vi": {
    "mapBased": {
      "rank": 19,
      "score": 0.793296
    },
    "tokenBased": {
      "rank": 7,
      "score": 0.45
    },
    "treeBased": {
      "rank": 117,
      "score": 0.592593
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 15,
      "vi_rank": 19,
      "delta": -4,
      "exceeds_10pct": false
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 2,
      "vi_rank": 7,
      "delta": -5,
      "exceeds_10pct": false
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 7,
      "vi_rank": 117,
      "delta": -110,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `aiohttp.web_urldispatcher.AbstractRoute.url/Vi-1_v1.0.5.py`
- **new**: `aiohttp.web_urldispatcher.AbstractRoute.url/Vi_v1.1.0.py`
- **+3 / -0**

```diff
--- aiohttp.web_urldispatcher.AbstractRoute.url/Vi-1_v1.0.5.py
+++ aiohttp.web_urldispatcher.AbstractRoute.url/Vi_v1.1.0.py
@@ -1,3 +1,6 @@
     @abc.abstractmethod
     def url(self, **kwargs):
         
+        warnings.warn(".url(...) is deprecated, use .url_for instead",
+                      DeprecationWarning,
+                      stacklevel=3)
```

```json
{
  "old_file": "aiohttp.web_urldispatcher.AbstractRoute.url/Vi-1_v1.0.5.py",
  "new_file": "aiohttp.web_urldispatcher.AbstractRoute.url/Vi_v1.1.0.py",
  "lines_added": 3,
  "lines_removed": 0
}
```
