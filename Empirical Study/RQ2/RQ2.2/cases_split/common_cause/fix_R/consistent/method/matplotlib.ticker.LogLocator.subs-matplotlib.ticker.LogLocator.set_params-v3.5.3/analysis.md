# 一、突变情况分析

- **Total**: 4807
- **替代API**: `matplotlib.ticker.LogLocator.set_params`
- **10% 阈值**: 480.7

## Vi-1 (v3.5.3-v3.8.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 150 | 0.4602 |
| tokenBased | 1412 | 0.2967 |
| treeBased | 331 | 0.4514 |

## Vi (v3.6.0-v3.8.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 3400 | 0.3708 |
| tokenBased | 2754 | 0.1636 |
| treeBased | 3055 | 0.3690 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 150 | 3400 | -3250 | true |
| tokenBased | 1412 | 2754 | -1342 | true |
| treeBased | 331 | 3055 | -2724 | true |

```json
{
  "total": 4807,
  "replacement_api": "matplotlib.ticker.LogLocator.set_params",
  "threshold_10pct": 480.7,
  "vi_minus_1": {
    "mapBased": {
      "rank": 150,
      "score": 0.460174
    },
    "tokenBased": {
      "rank": 1412,
      "score": 0.296703
    },
    "treeBased": {
      "rank": 331,
      "score": 0.451389
    }
  },
  "vi": {
    "mapBased": {
      "rank": 3400,
      "score": 0.370833
    },
    "tokenBased": {
      "rank": 2754,
      "score": 0.163636
    },
    "treeBased": {
      "rank": 3055,
      "score": 0.369048
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 150,
      "vi_rank": 3400,
      "delta": -3250,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 1412,
      "vi_rank": 2754,
      "delta": -1342,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 331,
      "vi_rank": 3055,
      "delta": -2724,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `matplotlib.ticker.LogLocator.subs/Vi-1_v3.5.3.py`
- **new**: `matplotlib.ticker.LogLocator.subs/Vi_v3.6.0.py`
- **+2 / -16**

```diff
--- matplotlib.ticker.LogLocator.subs/Vi-1_v3.5.3.py
+++ matplotlib.ticker.LogLocator.subs/Vi_v3.6.0.py
@@ -1,18 +1,4 @@
+    @_api.deprecated("3.6", alternative='set_params(subs=...)')
     def subs(self, subs):
         
-        if subs is None:
-            self._subs = 'auto'
-        elif isinstance(subs, str):
-            _api.check_in_list(('all', 'auto'), subs=subs)
-            self._subs = subs
-        else:
-            try:
-                self._subs = np.asarray(subs, dtype=float)
-            except ValueError as e:
-                raise ValueError("subs must be None, 'all', 'auto' or "
-                                 "a sequence of floats, not "
-                                 "{}.".format(subs)) from e
-            if self._subs.ndim != 1:
-                raise ValueError("A sequence passed to subs must be "
-                                 "1-dimensional, not "
-                                 "{}-dimensional.".format(self._subs.ndim))
+        self._set_subs(subs)
```

```json
{
  "old_file": "matplotlib.ticker.LogLocator.subs/Vi-1_v3.5.3.py",
  "new_file": "matplotlib.ticker.LogLocator.subs/Vi_v3.6.0.py",
  "lines_added": 2,
  "lines_removed": 16
}
```
