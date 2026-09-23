# 一、突变情况分析

- **Total**: 93
- **替代API**: `pydantic.main.BaseModel.dict`
- **10% 阈值**: 9.3

## Vi-1 (v0.5-v0.11.2)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 1 | 1.0000 |
| tokenBased | 1 | 0.8605 |
| treeBased | 1 | 0.9889 |

## Vi (v0.5-v0.12)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 24 | 0.6469 |
| tokenBased | 1 | 0.5217 |
| treeBased | 1 | 0.7522 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 1 | 24 | -23 | true |
| tokenBased | 1 | 1 | +0 | false |
| treeBased | 1 | 1 | +0 | false |

```json
{
  "total": 93,
  "replacement_api": "pydantic.main.BaseModel.dict",
  "threshold_10pct": 9.3,
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
      "rank": 24,
      "score": 0.646925
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.521739
    },
    "treeBased": {
      "rank": 1,
      "score": 0.752212
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 1,
      "vi_rank": 24,
      "delta": -23,
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
      "vi1_rank": 1,
      "vi_rank": 1,
      "delta": 0,
      "exceeds_10pct": false
    }
  ]
}
```

# 二、old → new Diff

- **old**: `R_candidates/Vi-1_v0.11.2/pydantic.main.BaseModel.dict.py`
- **new**: `R_candidates/Vi_v0.12/pydantic.main.BaseModel.dict.py`
- **+6 / -2**

```diff
--- R_candidates/Vi-1_v0.11.2/pydantic.main.BaseModel.dict.py
+++ R_candidates/Vi_v0.12/pydantic.main.BaseModel.dict.py
@@ -1,6 +1,10 @@
-    def dict(self, *, include: Set[str]=None, exclude: Set[str]=set()) -> Dict[str, Any]:
+    def dict(self, *, include: Set[str]=None, exclude: Set[str]=set(), by_alias: bool = False) -> Dict[str, Any]:
         
+        get_key = self._get_key_factory(by_alias)
+        get_key = partial(get_key, self.fields)
+
         return {
-            k: v for k, v in self
+            get_key(k): v
+            for k, v in self._iter(by_alias=by_alias)
             if k not in exclude and (not include or k in include)
         }
```

```json
{
  "old_file": "R_candidates/Vi-1_v0.11.2/pydantic.main.BaseModel.dict.py",
  "new_file": "R_candidates/Vi_v0.12/pydantic.main.BaseModel.dict.py",
  "lines_added": 6,
  "lines_removed": 2
}
```
