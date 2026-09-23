# 一、突变情况分析

- **Total**: 2513
- **替代API**: `pandas.core.categorical.Categorical.sort_values`
- **10% 阈值**: 251.3

## Vi-1 (v0.16.3-v0.21.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 1 | 0.8309 |
| tokenBased | 1 | 0.8590 |
| treeBased | 1 | 0.8314 |

## Vi (v0.17.0-v0.21.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 2186 | 0.2717 |
| tokenBased | 2201 | 0.1299 |
| treeBased | 2198 | 0.2525 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 1 | 2186 | -2185 | true |
| tokenBased | 1 | 2201 | -2200 | true |
| treeBased | 1 | 2198 | -2197 | true |

```json
{
  "total": 2513,
  "replacement_api": "pandas.core.categorical.Categorical.sort_values",
  "threshold_10pct": 251.3,
  "vi_minus_1": {
    "mapBased": {
      "rank": 1,
      "score": 0.830931
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.858974
    },
    "treeBased": {
      "rank": 1,
      "score": 0.831361
    }
  },
  "vi": {
    "mapBased": {
      "rank": 2186,
      "score": 0.271652
    },
    "tokenBased": {
      "rank": 2201,
      "score": 0.12987
    },
    "treeBased": {
      "rank": 2198,
      "score": 0.252475
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 1,
      "vi_rank": 2186,
      "delta": -2185,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 1,
      "vi_rank": 2201,
      "delta": -2200,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 1,
      "vi_rank": 2198,
      "delta": -2197,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `pandas.core.categorical.Categorical.order/Vi-1_v0.16.3.py`
- **new**: `pandas.core.categorical.Categorical.order/Vi_v0.17.0.py`
- **+3 / -30**

```diff
--- pandas.core.categorical.Categorical.order/Vi-1_v0.16.3.py
+++ pandas.core.categorical.Categorical.order/Vi_v0.17.0.py
@@ -1,32 +1,5 @@
     def order(self, inplace=False, ascending=True, na_position='last'):
         
-        if na_position not in ['last','first']:
-            raise ValueError('invalid na_position: {!r}'.format(na_position))
-
-        codes = np.sort(self._codes)
-        if not ascending:
-            codes = codes[::-1]
-
-
-        na_mask = (codes==-1)
-        if na_mask.any():
-            n_nans = len(codes[na_mask])
-            if na_position=="first" and not ascending:
-
-                new_codes = codes.copy()
-                new_codes[0:n_nans] = -1
-                new_codes[n_nans:] = codes[~na_mask]
-                codes = new_codes
-            elif na_position=="last" and not ascending:
-
-                new_codes = codes.copy()
-                pos = len(codes)-n_nans
-                new_codes[0:pos] = codes[~na_mask]
-                new_codes[pos:] = -1
-                codes = new_codes
-        if inplace:
-            self._codes = codes
-            return
-        else:
-            return Categorical(values=codes,categories=self.categories, ordered=self.ordered,
-                               name=self.name, fastpath=True)
+        warn("order is deprecated, use sort_values(...)",
+             FutureWarning, stacklevel=2)
+        return self.sort_values(inplace=inplace, ascending=ascending, na_position=na_position)
```

```json
{
  "old_file": "pandas.core.categorical.Categorical.order/Vi-1_v0.16.3.py",
  "new_file": "pandas.core.categorical.Categorical.order/Vi_v0.17.0.py",
  "lines_added": 3,
  "lines_removed": 30
}
```
