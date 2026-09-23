# 一、突变情况分析

- **Total**: 61
- **替代API**: `pydantic.main.BaseModel.dict`
- **10% 阈值**: 6.1

## Vi-1 (v0.1-v0.7)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 17 | 0.6751 |
| tokenBased | 30 | 0.1778 |
| treeBased | 40 | 0.2857 |

## Vi (v0.2-v0.7)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 1 | 1.0000 |
| tokenBased | 1 | 0.8605 |
| treeBased | 1 | 0.9889 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 17 | 1 | +16 | true |
| tokenBased | 30 | 1 | +29 | true |
| treeBased | 40 | 1 | +39 | true |

```json
{
  "total": 61,
  "replacement_api": "pydantic.main.BaseModel.dict",
  "threshold_10pct": 6.1,
  "vi_minus_1": {
    "mapBased": {
      "rank": 17,
      "score": 0.675115
    },
    "tokenBased": {
      "rank": 30,
      "score": 0.177778
    },
    "treeBased": {
      "rank": 40,
      "score": 0.285714
    }
  },
  "vi": {
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
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 17,
      "vi_rank": 1,
      "delta": 16,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 30,
      "vi_rank": 1,
      "delta": 29,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 40,
      "vi_rank": 1,
      "delta": 39,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `pydantic.main.BaseModel.values/Vi-1_v0.1.py`
- **new**: `pydantic.main.BaseModel.values/Vi_v0.2.py`
- **+6 / -3**

```diff
--- pydantic.main.BaseModel.values/Vi-1_v0.1.py
+++ pydantic.main.BaseModel.values/Vi_v0.2.py
@@ -1,3 +1,6 @@
-    @property
-    def values(self):
-        return dict(self)
+    def values(self, *, include: Set[str]=None, exclude: Set[str]=set()) -> Dict[str, Any]:
+        
+        return {
+            k: v for k, v in self
+            if k not in exclude and (not include or k in include)
+        }
```

```json
{
  "old_file": "pydantic.main.BaseModel.values/Vi-1_v0.1.py",
  "new_file": "pydantic.main.BaseModel.values/Vi_v0.2.py",
  "lines_added": 6,
  "lines_removed": 3
}
```
