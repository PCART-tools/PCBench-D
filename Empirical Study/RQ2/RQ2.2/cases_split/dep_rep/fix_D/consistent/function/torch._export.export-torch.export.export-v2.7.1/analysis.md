# 一、突变情况分析

- **Total**: 13392
- **替代API**: `torch.export.export`
- **10% 阈值**: 1339.2

## Vi-1 (v2.2.2-v2.7.1)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 325 | 0.7449 |
| tokenBased | 2 | 0.5385 |
| treeBased | 2 | 0.6860 |

## Vi (v2.2.2-v2.8.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 2496 | 0.5187 |
| tokenBased | 29 | 0.3532 |
| treeBased | 329 | 0.4739 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 325 | 2496 | -2171 | true |
| tokenBased | 2 | 29 | -27 | false |
| treeBased | 2 | 329 | -327 | false |

```json
{
  "total": 13392,
  "replacement_api": "torch.export.export",
  "threshold_10pct": 1339.2,
  "vi_minus_1": {
    "mapBased": {
      "rank": 325,
      "score": 0.744881
    },
    "tokenBased": {
      "rank": 2,
      "score": 0.538462
    },
    "treeBased": {
      "rank": 2,
      "score": 0.686047
    }
  },
  "vi": {
    "mapBased": {
      "rank": 2496,
      "score": 0.51868
    },
    "tokenBased": {
      "rank": 29,
      "score": 0.353211
    },
    "treeBased": {
      "rank": 329,
      "score": 0.473896
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 325,
      "vi_rank": 2496,
      "delta": -2171,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 2,
      "vi_rank": 29,
      "delta": -27,
      "exceeds_10pct": false
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 2,
      "vi_rank": 329,
      "delta": -327,
      "exceeds_10pct": false
    }
  ]
}
```

# 二、old → new Diff

- **old**: `R_candidates/Vi-1_v2.7.1/torch.export.export.py`
- **new**: `R_candidates/Vi_v2.8.0/torch.export.export.py`
- **+37 / -10**

```diff
--- R_candidates/Vi-1_v2.7.1/torch.export.export.py
+++ R_candidates/Vi_v2.8.0/torch.export.export.py
@@ -4,7 +4,7 @@
     kwargs: Optional[dict[str, Any]] = None,
     *,
     dynamic_shapes: Optional[Union[dict[str, Any], tuple[Any], list[Any]]] = None,
-    strict: bool = True,
+    strict: bool = False,
     preserve_module_call_signature: tuple[str, ...] = (),
 ) -> ExportedProgram:
     
@@ -20,12 +20,39 @@
             "Maybe try converting your ScriptModule to an ExportedProgram "
             "using `TS2EPConverter(mod, args, kwargs).convert()` instead."
         )
-    return _export(
-        mod,
-        args,
-        kwargs,
-        dynamic_shapes,
-        strict=strict,
-        preserve_module_call_signature=preserve_module_call_signature,
-        pre_dispatch=True,
-    )
+
+    try:
+        return _export(
+            mod,
+            args,
+            kwargs,
+            dynamic_shapes,
+            strict=strict,
+            preserve_module_call_signature=preserve_module_call_signature,
+            pre_dispatch=True,
+        )
+    except Exception as e:
+        draft_export_msg = (
+            "The error above occurred when calling torch.export.export. If you would "
+            "like to view some more information about this error, and get a list "
+            "of all other errors that may occur in your export call, you can "
+            "replace your `export()` call with `draft_export()`."
+        )
+
+
+
+        if isinstance(
+            e,
+            (
+                torch.fx.experimental.symbolic_shapes.GuardOnDataDependentSymNode,
+                torch._subclasses.fake_tensor.UnsupportedOperatorException,
+                torch._dynamo.exc.UserError,
+                torch.fx.experimental.symbolic_shapes.ConstraintViolationError,
+            ),
+        ):
+            new_msg = str(e) + "\n\n" + draft_export_msg
+            e.args = (new_msg,)
+        elif isinstance(e, RuntimeError) and "no fake impl registered" in str(e):
+            new_msg = str(e) + "\n\n" + draft_export_msg
+            e.args = (new_msg,)
+        raise e
```

```json
{
  "old_file": "R_candidates/Vi-1_v2.7.1/torch.export.export.py",
  "new_file": "R_candidates/Vi_v2.8.0/torch.export.export.py",
  "lines_added": 37,
  "lines_removed": 10
}
```
