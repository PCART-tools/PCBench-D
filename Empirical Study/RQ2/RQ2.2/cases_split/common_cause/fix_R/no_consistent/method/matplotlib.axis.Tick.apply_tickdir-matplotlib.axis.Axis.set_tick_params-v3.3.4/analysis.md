# 一、突变情况分析

- **Total**: 4803
- **替代API**: `matplotlib.axis.Axis.set_tick_params`
- **10% 阈值**: 480.3

## Vi-1 (v3.3.4-v3.7.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 4350 | 0.1581 |
| tokenBased | 4376 | 0.0336 |
| treeBased | 4467 | 0.0734 |

## Vi (v3.4.0-v3.7.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 4484 | 0.2510 |
| tokenBased | 2823 | 0.2065 |
| treeBased | 3588 | 0.3091 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 4350 | 4484 | -134 | false |
| tokenBased | 4376 | 2823 | +1553 | true |
| treeBased | 4467 | 3588 | +879 | true |

```json
{
  "total": 4803,
  "replacement_api": "matplotlib.axis.Axis.set_tick_params",
  "threshold_10pct": 480.3,
  "vi_minus_1": {
    "mapBased": {
      "rank": 4350,
      "score": 0.158129
    },
    "tokenBased": {
      "rank": 4376,
      "score": 0.033557
    },
    "treeBased": {
      "rank": 4467,
      "score": 0.073446
    }
  },
  "vi": {
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
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 4350,
      "vi_rank": 4484,
      "delta": -134,
      "exceeds_10pct": false
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 4376,
      "vi_rank": 2823,
      "delta": 1553,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 4467,
      "vi_rank": 3588,
      "delta": 879,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `matplotlib.axis.Tick.apply_tickdir/Vi-1_v3.3.4.py`
- **new**: `matplotlib.axis.Tick.apply_tickdir/Vi_v3.4.0.py`
- **+6 / -0**

```diff
--- matplotlib.axis.Tick.apply_tickdir/Vi-1_v3.3.4.py
+++ matplotlib.axis.Tick.apply_tickdir/Vi_v3.4.0.py
@@ -1,2 +1,8 @@
     def apply_tickdir(self, tickdir):
         
+        if tickdir is None:
+            tickdir = mpl.rcParams[f'{self.__name__}.direction']
+        _api.check_in_list(['in', 'out', 'inout'], tickdir=tickdir)
+        self._tickdir = tickdir
+        self._pad = self._base_pad + self.get_tick_padding()
+        self.stale = True
```

```json
{
  "old_file": "matplotlib.axis.Tick.apply_tickdir/Vi-1_v3.3.4.py",
  "new_file": "matplotlib.axis.Tick.apply_tickdir/Vi_v3.4.0.py",
  "lines_added": 6,
  "lines_removed": 0
}
```
