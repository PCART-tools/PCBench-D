# 一、突变情况分析

- **Total**: 73
- **替代API**: `httpx._config.Limits`
- **10% 阈值**: 7.3

## Vi-1 (0.13.3-0.15.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 1 | 0.6194 |
| tokenBased | 1 | 0.6917 |

## Vi (0.14.0-0.15.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 49 | 0.1226 |
| tokenBased | 12 | 0.2688 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 1 | 49 | -48 | true |
| tokenBased | 1 | 12 | -11 | true |

```json
{
  "total": 73,
  "replacement_api": "httpx._config.Limits",
  "threshold_10pct": 7.3,
  "vi_minus_1": {
    "mapBased": {
      "rank": 1,
      "score": 0.619352
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.691667
    }
  },
  "vi": {
    "mapBased": {
      "rank": 49,
      "score": 0.122646
    },
    "tokenBased": {
      "rank": 12,
      "score": 0.268817
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 1,
      "vi_rank": 49,
      "delta": -48,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 1,
      "vi_rank": 12,
      "delta": -11,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `httpx._config.PoolLimits/Vi-1_0.13.3.py`
- **new**: `httpx._config.PoolLimits/Vi_0.14.0.py`
- **+6 / -34**

```diff
--- httpx._config.PoolLimits/Vi-1_0.13.3.py
+++ httpx._config.PoolLimits/Vi_0.14.0.py
@@ -1,35 +1,7 @@
-class PoolLimits:
-    
-
-    def __init__(
-        self,
-        *,
-        max_keepalive: int = None,
-        max_connections: int = None,
-        soft_limit: int = None,
-        hard_limit: int = None,
-    ):
-        self.max_keepalive = max_keepalive
-        self.max_connections = max_connections
-        if soft_limit is not None:
-            self.max_keepalive = soft_limit
-            warn_deprecated("'soft_limit' is deprecated. Use 'max_keepalive' instead.",)
-        if hard_limit is not None:
-            self.max_connections = hard_limit
-            warn_deprecated(
-                "'hard_limit' is deprecated. Use 'max_connections' instead.",
-            )
-
-    def __eq__(self, other: typing.Any) -> bool:
-        return (
-            isinstance(other, self.__class__)
-            and self.max_keepalive == other.max_keepalive
-            and self.max_connections == other.max_connections
+class PoolLimits(Limits):
+    def __init__(self, **kwargs: typing.Any) -> None:
+        warn_deprecated(
+            "httpx.PoolLimits(...) is deprecated and will raise errors in the future. "
+            "Use httpx.Limits(...) instead."
         )
-
-    def __repr__(self) -> str:
-        class_name = self.__class__.__name__
-        return (
-            f"{class_name}(max_keepalive={self.max_keepalive}, "
-            f"max_connections={self.max_connections})"
-        )
+        super().__init__(**kwargs)
```

```json
{
  "old_file": "httpx._config.PoolLimits/Vi-1_0.13.3.py",
  "new_file": "httpx._config.PoolLimits/Vi_0.14.0.py",
  "lines_added": 6,
  "lines_removed": 34
}
```
