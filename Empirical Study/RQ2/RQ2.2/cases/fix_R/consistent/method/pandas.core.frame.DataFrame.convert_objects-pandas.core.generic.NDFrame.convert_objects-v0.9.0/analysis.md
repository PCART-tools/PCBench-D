# 一、突变情况分析

- **Total**: 1231
- **替代API**: `pandas.core.generic.NDFrame.convert_objects`
- **10% 阈值**: 123.1

## Vi-1 (v0.9.0-v0.13.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 444 | 0.4402 |
| tokenBased | 217 | 0.3684 |
| treeBased | 701 | 0.3457 |

## Vi (v0.9.1-v0.13.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 484 | 0.4153 |
| tokenBased | 373 | 0.3231 |
| treeBased | 726 | 0.3297 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 444 | 484 | -40 | false |
| tokenBased | 217 | 373 | -156 | true |
| treeBased | 701 | 726 | -25 | false |

```json
{
  "total": 1231,
  "replacement_api": "pandas.core.generic.NDFrame.convert_objects",
  "threshold_10pct": 123.1,
  "vi_minus_1": {
    "mapBased": {
      "rank": 444,
      "score": 0.440191
    },
    "tokenBased": {
      "rank": 217,
      "score": 0.368421
    },
    "treeBased": {
      "rank": 701,
      "score": 0.345679
    }
  },
  "vi": {
    "mapBased": {
      "rank": 484,
      "score": 0.41535
    },
    "tokenBased": {
      "rank": 373,
      "score": 0.323077
    },
    "treeBased": {
      "rank": 726,
      "score": 0.32967
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 444,
      "vi_rank": 484,
      "delta": -40,
      "exceeds_10pct": false
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 217,
      "vi_rank": 373,
      "delta": -156,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 701,
      "vi_rank": 726,
      "delta": -25,
      "exceeds_10pct": false
    }
  ]
}
```

# 二、old → new Diff

- **old**: `pandas.core.frame.DataFrame.convert_objects/Vi-1_v0.9.0.py`
- **new**: `pandas.core.frame.DataFrame.convert_objects/Vi_v0.9.1.py`
- **+2 / -1**

```diff
--- pandas.core.frame.DataFrame.convert_objects/Vi-1_v0.9.0.py
+++ pandas.core.frame.DataFrame.convert_objects/Vi_v0.9.1.py
@@ -2,11 +2,12 @@
     def convert_objects(self):
         
         new_data = {}
+        convert_f = lambda x: lib.maybe_convert_objects(x, convert_datetime=1)
 
 
         for col, s in self.iteritems():
             if s.dtype == np.object_:
-                new_data[col] = lib.maybe_convert_objects(s)
+                new_data[col] = convert_f(s)
             else:
                 new_data[col] = s
 
```

```json
{
  "old_file": "pandas.core.frame.DataFrame.convert_objects/Vi-1_v0.9.0.py",
  "new_file": "pandas.core.frame.DataFrame.convert_objects/Vi_v0.9.1.py",
  "lines_added": 2,
  "lines_removed": 1
}
```
