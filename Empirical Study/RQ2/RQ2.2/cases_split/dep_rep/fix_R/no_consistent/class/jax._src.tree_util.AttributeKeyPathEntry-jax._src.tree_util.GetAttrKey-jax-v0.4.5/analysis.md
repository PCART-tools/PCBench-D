# 一、突变情况分析

- **Total**: 430
- **替代API**: `jax._src.tree_util.GetAttrKey`
- **10% 阈值**: 43.0

## Vi-1 (jax-v0.4.5-jax-v0.4.24)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 27 | 0.5100 |
| tokenBased | 3 | 0.3846 |

## Vi (jax-v0.4.6-jax-v0.4.24)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 111 | 0.2948 |
| tokenBased | 3 | 0.3830 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 27 | 111 | -84 | true |
| tokenBased | 3 | 3 | +0 | false |

```json
{
  "total": 430,
  "replacement_api": "jax._src.tree_util.GetAttrKey",
  "threshold_10pct": 43.0,
  "vi_minus_1": {
    "mapBased": {
      "rank": 27,
      "score": 0.51
    },
    "tokenBased": {
      "rank": 3,
      "score": 0.384615
    }
  },
  "vi": {
    "mapBased": {
      "rank": 111,
      "score": 0.29475
    },
    "tokenBased": {
      "rank": 3,
      "score": 0.382979
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 27,
      "vi_rank": 111,
      "delta": -84,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 3,
      "vi_rank": 3,
      "delta": 0,
      "exceeds_10pct": false
    }
  ]
}
```

# 二、old → new Diff

- **old**: `jax._src.tree_util.AttributeKeyPathEntry/Vi-1_jax-v0.4.5.py`
- **new**: `jax._src.tree_util.AttributeKeyPathEntry/Vi_jax-v0.4.6.py`
- **+3 / -1**

```diff
--- jax._src.tree_util.AttributeKeyPathEntry/Vi-1_jax-v0.4.5.py
+++ jax._src.tree_util.AttributeKeyPathEntry/Vi_jax-v0.4.6.py
@@ -1,3 +1,5 @@
-class AttributeKeyPathEntry(KeyPathEntry):
+class AttributeKeyPathEntry(_DeprecatedKeyPathEntry):
   def pprint(self) -> str:
     return f'.{self.key}'
+  def __str__(self):
+    return self.pprint()
```

```json
{
  "old_file": "jax._src.tree_util.AttributeKeyPathEntry/Vi-1_jax-v0.4.5.py",
  "new_file": "jax._src.tree_util.AttributeKeyPathEntry/Vi_jax-v0.4.6.py",
  "lines_added": 3,
  "lines_removed": 1
}
```
