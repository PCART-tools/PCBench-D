# 一、突变情况分析

- **Total**: 61
- **替代API**: `pydantic.main.BaseModel.dict`
- **10% 阈值**: 6.1

## Vi-1 (v0.5-v0.7)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 1 | 1.0000 |
| tokenBased | 1 | 0.8605 |
| treeBased | 1 | 0.9889 |

## Vi (v0.6-v0.7)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 17 | 0.7500 |
| tokenBased | 35 | 0.1800 |
| treeBased | 44 | 0.3281 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 1 | 17 | -16 | true |
| tokenBased | 1 | 35 | -34 | true |
| treeBased | 1 | 44 | -43 | true |

```json
{
  "total": 61,
  "replacement_api": "pydantic.main.BaseModel.dict",
  "threshold_10pct": 6.1,
  "vi_minus_1": {
    "mapBased": {
      "rank": 1,
      "score": 1.0
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.860465
    },
    "treeBased": {
      "rank": 1,
      "score": 0.988889
    }
  },
  "vi": {
    "mapBased": {
      "rank": 17,
      "score": 0.75
    },
    "tokenBased": {
      "rank": 35,
      "score": 0.18
    },
    "treeBased": {
      "rank": 44,
      "score": 0.328125
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 1,
      "vi_rank": 17,
      "delta": -16,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 1,
      "vi_rank": 35,
      "delta": -34,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 1,
      "vi_rank": 44,
      "delta": -43,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `pydantic.main.BaseModel.values/Vi-1_v0.5.py`
- **new**: `pydantic.main.BaseModel.values/Vi_v0.6.py`
- **+4 / -6**

```diff
--- pydantic.main.BaseModel.values/Vi-1_v0.5.py
+++ pydantic.main.BaseModel.values/Vi_v0.6.py
@@ -1,6 +1,4 @@
-    def values(self, *, include: Set[str]=None, exclude: Set[str]=set()) -> Dict[str, Any]:
-        
-        return {
-            k: v for k, v in self
-            if k not in exclude and (not include or k in include)
-        }
+    def values(self, **kwargs):
+        warnings.warn('.values(...) is depreciated and will be removed in future, '
+                      'it has been replaced by .dict(...)', DeprecationWarning)
+        return self.dict(**kwargs)
```

```json
{
  "old_file": "pydantic.main.BaseModel.values/Vi-1_v0.5.py",
  "new_file": "pydantic.main.BaseModel.values/Vi_v0.6.py",
  "lines_added": 4,
  "lines_removed": 6
}
```
