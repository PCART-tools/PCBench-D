# 一、突变情况分析

- **Total**: 1231
- **替代API**: `pandas.core.generic.NDFrame.fillna`
- **10% 阈值**: 123.1

## Vi-1 (v0.9.1-v0.13.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 1164 | 0.2269 |
| tokenBased | 905 | 0.1753 |
| treeBased | 1100 | 0.2449 |

## Vi (v0.10.0-v0.13.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 944 | 0.2700 |
| tokenBased | 676 | 0.2371 |
| treeBased | 757 | 0.3325 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 1164 | 944 | +220 | true |
| tokenBased | 905 | 676 | +229 | true |
| treeBased | 1100 | 757 | +343 | true |

```json
{
  "total": 1231,
  "replacement_api": "pandas.core.generic.NDFrame.fillna",
  "threshold_10pct": 123.1,
  "vi_minus_1": {
    "mapBased": {
      "rank": 1164,
      "score": 0.226924
    },
    "tokenBased": {
      "rank": 905,
      "score": 0.175258
    },
    "treeBased": {
      "rank": 1100,
      "score": 0.244898
    }
  },
  "vi": {
    "mapBased": {
      "rank": 944,
      "score": 0.27002
    },
    "tokenBased": {
      "rank": 676,
      "score": 0.237113
    },
    "treeBased": {
      "rank": 757,
      "score": 0.332524
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 1164,
      "vi_rank": 944,
      "delta": 220,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 905,
      "vi_rank": 676,
      "delta": 229,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 1100,
      "vi_rank": 757,
      "delta": 343,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `pandas.core.panel.Panel.fillna/Vi-1_v0.9.1.py`
- **new**: `pandas.core.panel.Panel.fillna/Vi_v0.10.0.py`
- **+5 / -1**

```diff
--- pandas.core.panel.Panel.fillna/Vi-1_v0.9.1.py
+++ pandas.core.panel.Panel.fillna/Vi_v0.10.0.py
@@ -1,11 +1,15 @@
-    def fillna(self, value=None, method='pad'):
+    def fillna(self, value=None, method=None):
         
         if value is None:
+            if method is None:
+                raise ValueError('must specify a fill method or value')
             result = {}
             for col, s in self.iterkv():
                 result[col] = s.fillna(method=method, value=value)
 
             return self._constructor.from_dict(result)
         else:
+            if method is not None:
+                raise ValueError('cannot specify both a fill method and value')
             new_data = self._data.fillna(value)
             return self._constructor(new_data)
```

```json
{
  "old_file": "pandas.core.panel.Panel.fillna/Vi-1_v0.9.1.py",
  "new_file": "pandas.core.panel.Panel.fillna/Vi_v0.10.0.py",
  "lines_added": 5,
  "lines_removed": 1
}
```
