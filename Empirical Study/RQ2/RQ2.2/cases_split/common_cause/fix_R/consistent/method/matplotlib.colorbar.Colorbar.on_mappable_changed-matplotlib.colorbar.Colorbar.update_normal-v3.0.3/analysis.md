# 一、突变情况分析

- **Total**: 4823
- **替代API**: `matplotlib.colorbar.Colorbar.update_normal`
- **10% 阈值**: 482.3

## Vi-1 (v3.0.3-v3.5.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 1835 | 0.4535 |
| tokenBased | 1993 | 0.2169 |
| treeBased | 3442 | 0.4000 |

## Vi (v3.1.0-v3.5.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 2603 | 0.4418 |
| tokenBased | 3125 | 0.1646 |
| treeBased | 3561 | 0.3333 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 1835 | 2603 | -768 | true |
| tokenBased | 1993 | 3125 | -1132 | true |
| treeBased | 3442 | 3561 | -119 | false |

```json
{
  "total": 4823,
  "replacement_api": "matplotlib.colorbar.Colorbar.update_normal",
  "threshold_10pct": 482.3,
  "vi_minus_1": {
    "mapBased": {
      "rank": 1835,
      "score": 0.453451
    },
    "tokenBased": {
      "rank": 1993,
      "score": 0.216867
    },
    "treeBased": {
      "rank": 3442,
      "score": 0.4
    }
  },
  "vi": {
    "mapBased": {
      "rank": 2603,
      "score": 0.441769
    },
    "tokenBased": {
      "rank": 3125,
      "score": 0.164557
    },
    "treeBased": {
      "rank": 3561,
      "score": 0.333333
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 1835,
      "vi_rank": 2603,
      "delta": -768,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 1993,
      "vi_rank": 3125,
      "delta": -1132,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 3442,
      "vi_rank": 3561,
      "delta": -119,
      "exceeds_10pct": false
    }
  ]
}
```

# 二、old → new Diff

- **old**: `matplotlib.colorbar.Colorbar.on_mappable_changed/Vi-1_v3.0.3.py`
- **new**: `matplotlib.colorbar.Colorbar.on_mappable_changed/Vi_v3.1.0.py`
- **+1 / -2**

```diff
--- matplotlib.colorbar.Colorbar.on_mappable_changed/Vi-1_v3.0.3.py
+++ matplotlib.colorbar.Colorbar.on_mappable_changed/Vi_v3.1.0.py
@@ -1,5 +1,4 @@
     def on_mappable_changed(self, mappable):
         
-        self.set_cmap(mappable.get_cmap())
-        self.set_clim(mappable.get_clim())
+        _log.debug('colorbar mappable changed')
         self.update_normal(mappable)
```

```json
{
  "old_file": "matplotlib.colorbar.Colorbar.on_mappable_changed/Vi-1_v3.0.3.py",
  "new_file": "matplotlib.colorbar.Colorbar.on_mappable_changed/Vi_v3.1.0.py",
  "lines_added": 1,
  "lines_removed": 2
}
```
