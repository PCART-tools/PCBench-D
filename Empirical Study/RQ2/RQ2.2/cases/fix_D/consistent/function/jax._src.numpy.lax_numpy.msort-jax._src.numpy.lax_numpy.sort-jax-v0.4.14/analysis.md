# 一、突变情况分析

- **Total**: 467
- **替代API**: `jax._src.numpy.lax_numpy.sort`
- **10% 阈值**: 46.7

## Vi-1 (jax-v0.4.0-jax-v0.4.14)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 230 | 0.4036 |
| tokenBased | 109 | 0.2099 |
| treeBased | 215 | 0.3333 |

## Vi (jax-v0.4.0-jax-v0.4.15)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 231 | 0.4036 |
| tokenBased | 163 | 0.1789 |
| treeBased | 247 | 0.3130 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 230 | 231 | -1 | false |
| tokenBased | 109 | 163 | -54 | true |
| treeBased | 215 | 247 | -32 | false |

```json
{
  "total": 467,
  "replacement_api": "jax._src.numpy.lax_numpy.sort",
  "threshold_10pct": 46.7,
  "vi_minus_1": {
    "mapBased": {
      "rank": 230,
      "score": 0.40364
    },
    "tokenBased": {
      "rank": 109,
      "score": 0.209877
    },
    "treeBased": {
      "rank": 215,
      "score": 0.333333
    }
  },
  "vi": {
    "mapBased": {
      "rank": 231,
      "score": 0.40364
    },
    "tokenBased": {
      "rank": 163,
      "score": 0.178947
    },
    "treeBased": {
      "rank": 247,
      "score": 0.313043
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 230,
      "vi_rank": 231,
      "delta": -1,
      "exceeds_10pct": false
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 109,
      "vi_rank": 163,
      "delta": -54,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 215,
      "vi_rank": 247,
      "delta": -32,
      "exceeds_10pct": false
    }
  ]
}
```

# 二、old → new Diff

- **old**: `R_candidates/Vi-1_jax-v0.4.14/jax._src.numpy.lax_numpy.sort.py`
- **new**: `R_candidates/Vi_jax-v0.4.15/jax._src.numpy.lax_numpy.sort.py`
- **+6 / -1**

```diff
--- R_candidates/Vi-1_jax-v0.4.14/jax._src.numpy.lax_numpy.sort.py
+++ R_candidates/Vi_jax-v0.4.15/jax._src.numpy.lax_numpy.sort.py
@@ -1,6 +1,11 @@
 @util._wraps(np.sort)
 @partial(jit, static_argnames=('axis', 'kind', 'order'))
-def sort(a, axis: Optional[int] = -1, kind='quicksort', order=None):
+def sort(
+    a: ArrayLike,
+    axis: int | None = -1,
+    kind: str = "quicksort",
+    order: None = None,
+) -> Array:
   util.check_arraylike("sort", a)
   if kind != 'quicksort':
     warnings.warn("'kind' argument to sort is ignored.")
```

```json
{
  "old_file": "R_candidates/Vi-1_jax-v0.4.14/jax._src.numpy.lax_numpy.sort.py",
  "new_file": "R_candidates/Vi_jax-v0.4.15/jax._src.numpy.lax_numpy.sort.py",
  "lines_added": 6,
  "lines_removed": 1
}
```
