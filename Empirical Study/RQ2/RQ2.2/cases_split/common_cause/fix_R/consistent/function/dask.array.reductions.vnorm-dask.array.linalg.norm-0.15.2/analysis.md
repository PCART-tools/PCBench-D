# 一、突变情况分析

- **Total**: 1087
- **替代API**: `dask.array.linalg.norm`
- **10% 阈值**: 108.7

## Vi-1 (0.15.2-0.19.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 445 | 0.1356 |
| tokenBased | 364 | 0.2659 |
| treeBased | 130 | 0.3629 |

## Vi (0.15.3-0.19.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 473 | 0.1261 |
| tokenBased | 631 | 0.2211 |
| treeBased | 526 | 0.3216 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 445 | 473 | -28 | false |
| tokenBased | 364 | 631 | -267 | true |
| treeBased | 130 | 526 | -396 | true |

```json
{
  "total": 1087,
  "replacement_api": "dask.array.linalg.norm",
  "threshold_10pct": 108.7,
  "vi_minus_1": {
    "mapBased": {
      "rank": 445,
      "score": 0.135595
    },
    "tokenBased": {
      "rank": 364,
      "score": 0.265854
    },
    "treeBased": {
      "rank": 130,
      "score": 0.362876
    }
  },
  "vi": {
    "mapBased": {
      "rank": 473,
      "score": 0.126068
    },
    "tokenBased": {
      "rank": 631,
      "score": 0.22113
    },
    "treeBased": {
      "rank": 526,
      "score": 0.321617
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 445,
      "vi_rank": 473,
      "delta": -28,
      "exceeds_10pct": false
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 364,
      "vi_rank": 631,
      "delta": -267,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 130,
      "vi_rank": 526,
      "delta": -396,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `dask.array.reductions.vnorm/Vi-1_0.15.2.py`
- **new**: `dask.array.reductions.vnorm/Vi_0.15.3.py`
- **+0 / -3**

```diff
--- dask.array.reductions.vnorm/Vi-1_0.15.2.py
+++ dask.array.reductions.vnorm/Vi_0.15.3.py
@@ -12,9 +12,6 @@
     elif ord == 1:
         return sum(abs(a), axis=axis, dtype=dtype, keepdims=keepdims,
                    split_every=split_every, out=out)
-    elif ord % 2 == 0:
-        return sum(a ** ord, axis=axis, dtype=dtype, keepdims=keepdims,
-                   split_every=split_every, out=out) ** (1. / ord)
     else:
         return sum(abs(a) ** ord, axis=axis, dtype=dtype, keepdims=keepdims,
                    split_every=split_every, out=out) ** (1. / ord)
```

```json
{
  "old_file": "dask.array.reductions.vnorm/Vi-1_0.15.2.py",
  "new_file": "dask.array.reductions.vnorm/Vi_0.15.3.py",
  "lines_added": 0,
  "lines_removed": 3
}
```
