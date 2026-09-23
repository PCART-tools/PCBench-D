# 一、突变情况分析

- **Total**: 4803
- **替代API**: `matplotlib.axis.Axis.set_tick_params`
- **10% 阈值**: 480.3

## Vi-1 (v3.4.3-v3.7.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 4484 | 0.2510 |
| tokenBased | 2823 | 0.2065 |
| treeBased | 3588 | 0.3091 |

## Vi (v3.5.0-v3.7.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 4369 | 0.2111 |
| tokenBased | 4326 | 0.0728 |
| treeBased | 4406 | 0.1823 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 4484 | 4369 | +115 | false |
| tokenBased | 2823 | 4326 | -1503 | true |
| treeBased | 3588 | 4406 | -818 | true |

```json
{
  "total": 4803,
  "replacement_api": "matplotlib.axis.Axis.set_tick_params",
  "threshold_10pct": 480.3,
  "vi_minus_1": {
    "mapBased": {
      "rank": 4484,
      "score": 0.250956
    },
    "tokenBased": {
      "rank": 2823,
      "score": 0.206452
    },
    "treeBased": {
      "rank": 3588,
      "score": 0.309091
    }
  },
  "vi": {
    "mapBased": {
      "rank": 4369,
      "score": 0.211055
    },
    "tokenBased": {
      "rank": 4326,
      "score": 0.072848
    },
    "treeBased": {
      "rank": 4406,
      "score": 0.182292
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 4484,
      "vi_rank": 4369,
      "delta": 115,
      "exceeds_10pct": false
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 2823,
      "vi_rank": 4326,
      "delta": -1503,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 3588,
      "vi_rank": 4406,
      "delta": -818,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `matplotlib.axis.Tick.apply_tickdir/Vi-1_v3.4.3.py`
- **new**: `matplotlib.axis.Tick.apply_tickdir/Vi_v3.5.0.py`
- **+2 / -6**

```diff
--- matplotlib.axis.Tick.apply_tickdir/Vi-1_v3.4.3.py
+++ matplotlib.axis.Tick.apply_tickdir/Vi_v3.5.0.py
@@ -1,8 +1,4 @@
+    @_api.deprecated("3.5", alternative="axis.set_tick_params")
     def apply_tickdir(self, tickdir):
-        
-        if tickdir is None:
-            tickdir = mpl.rcParams[f'{self.__name__}.direction']
-        _api.check_in_list(['in', 'out', 'inout'], tickdir=tickdir)
-        self._tickdir = tickdir
-        self._pad = self._base_pad + self.get_tick_padding()
+        self._apply_tickdir(tickdir)
         self.stale = True
```

```json
{
  "old_file": "matplotlib.axis.Tick.apply_tickdir/Vi-1_v3.4.3.py",
  "new_file": "matplotlib.axis.Tick.apply_tickdir/Vi_v3.5.0.py",
  "lines_added": 2,
  "lines_removed": 6
}
```
