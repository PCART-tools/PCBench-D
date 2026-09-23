# 一、突变情况分析

- **Total**: 1231
- **替代API**: `pandas.core.generic.NDFrame.convert_objects`
- **10% 阈值**: 123.1

## Vi-1 (v0.10.1-v0.13.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 302 | 0.4658 |
| tokenBased | 307 | 0.3538 |
| treeBased | 663 | 0.3617 |

## Vi (v0.11.0-v0.13.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 36 | 0.9191 |
| tokenBased | 1 | 0.7742 |
| treeBased | 1 | 0.8571 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 302 | 36 | +266 | true |
| tokenBased | 307 | 1 | +306 | true |
| treeBased | 663 | 1 | +662 | true |

```json
{
  "total": 1231,
  "replacement_api": "pandas.core.generic.NDFrame.convert_objects",
  "threshold_10pct": 123.1,
  "vi_minus_1": {
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
  "vi": {
    "mapBased": {
      "rank": 36,
      "score": 0.919094
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.774194
    },
    "treeBased": {
      "rank": 1,
      "score": 0.857143
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 302,
      "vi_rank": 36,
      "delta": 266,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 307,
      "vi_rank": 1,
      "delta": 306,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 663,
      "vi_rank": 1,
      "delta": 662,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `pandas.core.frame.DataFrame.convert_objects/Vi-1_v0.10.1.py`
- **new**: `pandas.core.frame.DataFrame.convert_objects/Vi_v0.11.0.py`
- **+2 / -13**

```diff
--- pandas.core.frame.DataFrame.convert_objects/Vi-1_v0.10.1.py
+++ pandas.core.frame.DataFrame.convert_objects/Vi_v0.11.0.py
@@ -1,15 +1,4 @@
 
-    def convert_objects(self, convert_dates=True):
+    def convert_objects(self, convert_dates=True, convert_numeric=False):
         
-        new_data = {}
-        convert_f = lambda x: lib.maybe_convert_objects(
-            x, convert_datetime=convert_dates)
-
-
-        for col, s in self.iteritems():
-            if s.dtype == np.object_:
-                new_data[col] = convert_f(s)
-            else:
-                new_data[col] = s
-
-        return DataFrame(new_data, index=self.index, columns=self.columns)
+        return self._constructor(self._data.convert(convert_dates=convert_dates, convert_numeric=convert_numeric))
```

```json
{
  "old_file": "pandas.core.frame.DataFrame.convert_objects/Vi-1_v0.10.1.py",
  "new_file": "pandas.core.frame.DataFrame.convert_objects/Vi_v0.11.0.py",
  "lines_added": 2,
  "lines_removed": 13
}
```
