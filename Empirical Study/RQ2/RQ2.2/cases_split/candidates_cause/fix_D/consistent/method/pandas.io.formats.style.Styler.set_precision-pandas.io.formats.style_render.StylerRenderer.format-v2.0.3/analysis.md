# 一、突变情况分析

- **Total**: 417
- **替代API**: `pandas.io.formats.style_render.StylerRenderer.format`
- **10% 阈值**: 41.7

## Vi-1 (v1.2.5-v2.0.3)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 378 | 0.2112 |
| tokenBased | 360 | 0.0737 |
| treeBased | 385 | 0.1202 |

## Vi (v1.2.5-v2.1.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 324 | 0.2112 |
| tokenBased | 310 | 0.0737 |
| treeBased | 334 | 0.1202 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 378 | 324 | +54 | true |
| tokenBased | 360 | 310 | +50 | true |
| treeBased | 385 | 334 | +51 | true |

```json
{
  "total": 417,
  "replacement_api": "pandas.io.formats.style_render.StylerRenderer.format",
  "threshold_10pct": 41.7,
  "vi_minus_1": {
    "mapBased": {
      "rank": 378,
      "score": 0.211155
    },
    "tokenBased": {
      "rank": 360,
      "score": 0.073733
    },
    "treeBased": {
      "rank": 385,
      "score": 0.120192
    }
  },
  "vi": {
    "mapBased": {
      "rank": 324,
      "score": 0.211155
    },
    "tokenBased": {
      "rank": 310,
      "score": 0.073733
    },
    "treeBased": {
      "rank": 334,
      "score": 0.120192
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 378,
      "vi_rank": 324,
      "delta": 54,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 360,
      "vi_rank": 310,
      "delta": 50,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 385,
      "vi_rank": 334,
      "delta": 51,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `R_candidates/Vi-1_v2.0.3/pandas.io.formats.style_render.StylerRenderer.format.py`
- **new**: `R_candidates/Vi_v2.1.0/pandas.io.formats.style_render.StylerRenderer.format.py`
- **+0 / -0**

```diff
```

```json
{
  "old_file": "R_candidates/Vi-1_v2.0.3/pandas.io.formats.style_render.StylerRenderer.format.py",
  "new_file": "R_candidates/Vi_v2.1.0/pandas.io.formats.style_render.StylerRenderer.format.py",
  "lines_added": 0,
  "lines_removed": 0
}
```
