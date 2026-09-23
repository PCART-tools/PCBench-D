# 一、突变情况分析

- **Total**: 417
- **替代API**: `pandas.io.formats.style.Styler.to_html`
- **10% 阈值**: 41.7

## Vi-1 (v1.2.5-v2.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 349 | 0.3120 |
| tokenBased | 377 | 0.1189 |
| treeBased | 365 | 0.2579 |

## Vi (v1.3.0-v2.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 245 | 0.3798 |
| tokenBased | 133 | 0.2298 |
| treeBased | 244 | 0.3468 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 349 | 245 | +104 | true |
| tokenBased | 377 | 133 | +244 | true |
| treeBased | 365 | 244 | +121 | true |

```json
{
  "total": 417,
  "replacement_api": "pandas.io.formats.style.Styler.to_html",
  "threshold_10pct": 41.7,
  "vi_minus_1": {
    "mapBased": {
      "rank": 349,
      "score": 0.312022
    },
    "tokenBased": {
      "rank": 377,
      "score": 0.118852
    },
    "treeBased": {
      "rank": 365,
      "score": 0.257937
    }
  },
  "vi": {
    "mapBased": {
      "rank": 245,
      "score": 0.379768
    },
    "tokenBased": {
      "rank": 133,
      "score": 0.229787
    },
    "treeBased": {
      "rank": 244,
      "score": 0.346774
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 349,
      "vi_rank": 245,
      "delta": 104,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 377,
      "vi_rank": 133,
      "delta": 244,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 365,
      "vi_rank": 244,
      "delta": 121,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `pandas.io.formats.style.Styler.render/Vi-1_v1.2.5.py`
- **new**: `pandas.io.formats.style.Styler.render/Vi_v1.3.0.py`
- **+11 / -11**

```diff
--- pandas.io.formats.style.Styler.render/Vi-1_v1.2.5.py
+++ pandas.io.formats.style.Styler.render/Vi_v1.3.0.py
@@ -1,12 +1,12 @@
-    def render(self, **kwargs) -> str:
+    def render(
+        self,
+        sparse_index: bool | None = None,
+        sparse_columns: bool | None = None,
+        **kwargs,
+    ) -> str:
         
-        self._compute()
-
-        d = self._translate()
-
-
-
-        trimmed = [x for x in d["cellstyle"] if any(any(y) for y in x["props"])]
-        d["cellstyle"] = trimmed
-        d.update(kwargs)
-        return self.template.render(**d)
+        if sparse_index is None:
+            sparse_index = get_option("styler.sparse.index")
+        if sparse_columns is None:
+            sparse_columns = get_option("styler.sparse.columns")
+        return self._render_html(sparse_index, sparse_columns, **kwargs)
```

```json
{
  "old_file": "pandas.io.formats.style.Styler.render/Vi-1_v1.2.5.py",
  "new_file": "pandas.io.formats.style.Styler.render/Vi_v1.3.0.py",
  "lines_added": 11,
  "lines_removed": 11
}
```
