# 一、突变情况分析

- **Total**: 1231
- **替代API**: `pandas.core.generic.NDFrame.convert_objects`
- **10% 阈值**: 123.1

## Vi-1 (v0.9.1-v0.13.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 484 | 0.4153 |
| tokenBased | 373 | 0.3231 |
| treeBased | 726 | 0.3297 |

## Vi (v0.10.0-v0.13.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 302 | 0.4658 |
| tokenBased | 307 | 0.3538 |
| treeBased | 663 | 0.3617 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 484 | 302 | +182 | true |
| tokenBased | 373 | 307 | +66 | false |
| treeBased | 726 | 663 | +63 | false |

```json
{
  "total": 1231,
  "replacement_api": "pandas.core.generic.NDFrame.convert_objects",
  "threshold_10pct": 123.1,
  "vi_minus_1": {
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
  "vi": {
    "mapBased": {
      "rank": 302,
      "score": 0.465812
    },
    "tokenBased": {
      "rank": 307,
      "score": 0.353846
    },
    "treeBased": {
      "rank": 663,
      "score": 0.361702
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 484,
      "vi_rank": 302,
      "delta": 182,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 373,
      "vi_rank": 307,
      "delta": 66,
      "exceeds_10pct": false
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 726,
      "vi_rank": 663,
      "delta": 63,
      "exceeds_10pct": false
    }
  ]
}
```

# 二、old → new Diff

- **old**: `pandas.core.frame.DataFrame.convert_objects/Vi-1_v0.9.1.py`
- **new**: `pandas.core.frame.DataFrame.convert_objects/Vi_v0.10.0.py`
- **+3 / -2**

```diff
--- pandas.core.frame.DataFrame.convert_objects/Vi-1_v0.9.1.py
+++ pandas.core.frame.DataFrame.convert_objects/Vi_v0.10.0.py
@@ -1,8 +1,9 @@
 
-    def convert_objects(self):
+    def convert_objects(self, convert_dates=True):
         
         new_data = {}
-        convert_f = lambda x: lib.maybe_convert_objects(x, convert_datetime=1)
+        convert_f = lambda x: lib.maybe_convert_objects(
+            x, convert_datetime=convert_dates)
 
 
         for col, s in self.iteritems():
```

```json
{
  "old_file": "pandas.core.frame.DataFrame.convert_objects/Vi-1_v0.9.1.py",
  "new_file": "pandas.core.frame.DataFrame.convert_objects/Vi_v0.10.0.py",
  "lines_added": 3,
  "lines_removed": 2
}
```
