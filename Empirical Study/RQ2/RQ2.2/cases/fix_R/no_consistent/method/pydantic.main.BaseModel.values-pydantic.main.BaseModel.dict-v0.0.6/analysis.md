# 一、突变情况分析

- **Total**: 61
- **替代API**: `pydantic.main.BaseModel.dict`
- **10% 阈值**: 6.1

## Vi-1 (v0.0.6-v0.7)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 17 | 0.6751 |
| tokenBased | 37 | 0.1111 |
| treeBased | 40 | 0.2727 |

## Vi (v0.0.7-v0.7)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 17 | 0.6751 |
| tokenBased | 30 | 0.1778 |
| treeBased | 40 | 0.2857 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 17 | 17 | +0 | false |
| tokenBased | 37 | 30 | +7 | true |
| treeBased | 40 | 40 | +0 | false |

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
      "rank": 37,
      "score": 0.111111
    },
    "treeBased": {
      "rank": 40,
      "score": 0.272727
    }
  },
  "vi": {
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
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 17,
      "vi_rank": 17,
      "delta": 0,
      "exceeds_10pct": false
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 37,
      "vi_rank": 30,
      "delta": 7,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 40,
      "vi_rank": 40,
      "delta": 0,
      "exceeds_10pct": false
    }
  ]
}
```

# 二、old → new Diff

- **old**: `pydantic.main.BaseModel.values/Vi-1_v0.0.6.py`
- **new**: `pydantic.main.BaseModel.values/Vi_v0.0.7.py`
- **+1 / -1**

```diff
--- pydantic.main.BaseModel.values/Vi-1_v0.0.6.py
+++ pydantic.main.BaseModel.values/Vi_v0.0.7.py
@@ -1,3 +1,3 @@
     @property
     def values(self):
-        return self.__values__
+        return dict(self)
```

```json
{
  "old_file": "pydantic.main.BaseModel.values/Vi-1_v0.0.6.py",
  "new_file": "pydantic.main.BaseModel.values/Vi_v0.0.7.py",
  "lines_added": 1,
  "lines_removed": 1
}
```
