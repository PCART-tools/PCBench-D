# 一、突变情况分析

- **Total**: 41
- **替代API**: `aiohttp.connector.UnixConnector`
- **10% 阈值**: 4.1

## Vi-1 (v0.7.0-v0.7.3)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 11 | 0.1883 |
| tokenBased | 26 | 0.1792 |

## Vi (v0.7.0-v0.8.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 14 | 0.1883 |
| tokenBased | 31 | 0.1792 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 11 | 14 | -3 | false |
| tokenBased | 26 | 31 | -5 | true |

```json
{
  "total": 41,
  "replacement_api": "aiohttp.connector.UnixConnector",
  "threshold_10pct": 4.1,
  "vi_minus_1": {
    "mapBased": {
      "rank": 11,
      "score": 0.188336
    },
    "tokenBased": {
      "rank": 26,
      "score": 0.179211
    }
  },
  "vi": {
    "mapBased": {
      "rank": 14,
      "score": 0.188336
    },
    "tokenBased": {
      "rank": 31,
      "score": 0.179211
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 11,
      "vi_rank": 14,
      "delta": -3,
      "exceeds_10pct": false
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 26,
      "vi_rank": 31,
      "delta": -5,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `R_candidates/Vi-1_v0.7.3/aiohttp.connector.UnixConnector.py`
- **new**: `R_candidates/Vi_v0.8.0/aiohttp.connector.UnixConnector.py`
- **+0 / -0**

```diff
```

```json
{
  "old_file": "R_candidates/Vi-1_v0.7.3/aiohttp.connector.UnixConnector.py",
  "new_file": "R_candidates/Vi_v0.8.0/aiohttp.connector.UnixConnector.py",
  "lines_added": 0,
  "lines_removed": 0
}
```
