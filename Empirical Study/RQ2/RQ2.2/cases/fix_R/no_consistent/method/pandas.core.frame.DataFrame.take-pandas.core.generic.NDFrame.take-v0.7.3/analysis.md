# 一、突变情况分析

- **Total**: 1231
- **替代API**: `pandas.core.generic.NDFrame.take`
- **10% 阈值**: 123.1

## Vi-1 (v0.7.3-v0.13.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 286 | 0.3748 |
| tokenBased | 1 | 0.6116 |
| treeBased | 33 | 0.5071 |

## Vi (v0.8.0-v0.13.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 61 | 0.4402 |
| tokenBased | 1 | 0.6640 |
| treeBased | 15 | 0.5202 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 286 | 61 | +225 | true |
| tokenBased | 1 | 1 | +0 | false |
| treeBased | 33 | 15 | +18 | false |

```json
{
  "total": 1231,
  "replacement_api": "pandas.core.generic.NDFrame.take",
  "threshold_10pct": 123.1,
  "vi_minus_1": {
    "mapBased": {
      "rank": 286,
      "score": 0.374832
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.61157
    },
    "treeBased": {
      "rank": 33,
      "score": 0.507109
    }
  },
  "vi": {
    "mapBased": {
      "rank": 61,
      "score": 0.440172
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.664
    },
    "treeBased": {
      "rank": 15,
      "score": 0.520179
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 286,
      "vi_rank": 61,
      "delta": 225,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 1,
      "vi_rank": 1,
      "delta": 0,
      "exceeds_10pct": false
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 33,
      "vi_rank": 15,
      "delta": 18,
      "exceeds_10pct": false
    }
  ]
}
```

# 二、old → new Diff

- **old**: `pandas.core.frame.DataFrame.take/Vi-1_v0.7.3.py`
- **new**: `pandas.core.frame.DataFrame.take/Vi_v0.8.0.py`
- **+3 / -1**

```diff
--- pandas.core.frame.DataFrame.take/Vi-1_v0.7.3.py
+++ pandas.core.frame.DataFrame.take/Vi_v0.8.0.py
@@ -1,6 +1,8 @@
 
     def take(self, indices, axis=0):
         
+        if isinstance(indices, list):
+            indices = np.array(indices)
         if self._data.is_mixed_dtype():
             if axis == 0:
                 new_data = self._data.take(indices, axis=1)
@@ -10,7 +12,7 @@
                 return self.reindex(columns=new_columns)
         else:
             new_values = com.take_2d(self.values,
-                                     com._ensure_int32(indices),
+                                     com._ensure_int64(indices),
                                      axis=axis)
             if axis == 0:
                 new_columns = self.columns
```

```json
{
  "old_file": "pandas.core.frame.DataFrame.take/Vi-1_v0.7.3.py",
  "new_file": "pandas.core.frame.DataFrame.take/Vi_v0.8.0.py",
  "lines_added": 3,
  "lines_removed": 1
}
```
