# 一、突变情况分析

- **Total**: 85
- **替代API**: `xgboost.core.QuantileDMatrix`
- **10% 阈值**: 8.5

## Vi-1 (v1.6.2-v3.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 1 | 0.7327 |
| tokenBased | 1 | 0.7318 |

## Vi (v1.7.0-v3.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 49 | 0.1148 |
| tokenBased | 67 | 0.0697 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 1 | 49 | -48 | true |
| tokenBased | 1 | 67 | -66 | true |

```json
{
  "total": 85,
  "replacement_api": "xgboost.core.QuantileDMatrix",
  "threshold_10pct": 8.5,
  "vi_minus_1": {
    "mapBased": {
      "rank": 1,
      "score": 0.73274
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.731755
    }
  },
  "vi": {
    "mapBased": {
      "rank": 49,
      "score": 0.114802
    },
    "tokenBased": {
      "rank": 67,
      "score": 0.069721
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
      "vi_rank": 67,
      "delta": -66,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `xgboost.core.DeviceQuantileDMatrix/Vi-1_v1.6.2.py`
- **new**: `xgboost.core.DeviceQuantileDMatrix/Vi_v1.7.0.py`
- **+4 / -90**

```diff
--- xgboost.core.DeviceQuantileDMatrix/Vi-1_v1.6.2.py
+++ xgboost.core.DeviceQuantileDMatrix/Vi_v1.7.0.py
@@ -1,92 +1,6 @@
-class DeviceQuantileDMatrix(DMatrix):
+class DeviceQuantileDMatrix(QuantileDMatrix):
     
 
-    @_deprecate_positional_args
-    def __init__(
-        self,
-        data: DataType,
-        label: Optional[ArrayLike] = None,
-        *,
-        weight: Optional[ArrayLike] = None,
-        base_margin: Optional[ArrayLike] = None,
-        missing: Optional[float] = None,
-        silent: bool = False,
-        feature_names: FeatureNames = None,
-        feature_types: Optional[List[str]] = None,
-        nthread: Optional[int] = None,
-        max_bin: int = 256,
-        group: Optional[ArrayLike] = None,
-        qid: Optional[ArrayLike] = None,
-        label_lower_bound: Optional[ArrayLike] = None,
-        label_upper_bound: Optional[ArrayLike] = None,
-        feature_weights: Optional[ArrayLike] = None,
-        enable_categorical: bool = False,
-    ) -> None:
-        self.max_bin = max_bin
-        self.missing = missing if missing is not None else np.nan
-        self.nthread = nthread if nthread is not None else 1
-        self._silent = silent
-
-        if isinstance(data, ctypes.c_void_p):
-            self.handle = data
-            return
-
-        if qid is not None and group is not None:
-            raise ValueError(
-                'Only one of the eval_qid or eval_group for each evaluation '
-                'dataset should be provided.'
-            )
-
-        self._init(
-            data,
-            label=label,
-            weight=weight,
-            base_margin=base_margin,
-            group=group,
-            qid=qid,
-            label_lower_bound=label_lower_bound,
-            label_upper_bound=label_upper_bound,
-            feature_weights=feature_weights,
-            feature_names=feature_names,
-            feature_types=feature_types,
-            enable_categorical=enable_categorical,
-        )
-
-    def _init(self, data: DataType, enable_categorical: bool, **meta: Any) -> None:
-        from .data import (
-            _is_dlpack,
-            _transform_dlpack,
-            _is_iter,
-            SingleBatchInternalIter,
-        )
-
-        if _is_dlpack(data):
-
-
-            data = _transform_dlpack(data)
-        if _is_iter(data):
-            it = data
-        else:
-            it = SingleBatchInternalIter(data=data, **meta)
-
-        handle = ctypes.c_void_p()
-        reset_callback, next_callback = it.get_callbacks(False, enable_categorical)
-        if it.cache_prefix is not None:
-            raise ValueError(
-                "DeviceQuantileDMatrix doesn't cache data, remove the cache_prefix "
-                "in iterator to fix this error."
-            )
-        ret = _LIB.XGDeviceQuantileDMatrixCreateFromCallback(
-            None,
-            it.proxy.handle,
-            reset_callback,
-            next_callback,
-            ctypes.c_float(self.missing),
-            ctypes.c_int(self.nthread),
-            ctypes.c_int(self.max_bin),
-            ctypes.byref(handle),
-        )
-        it.reraise()
-
-        _check_call(ret)
-        self.handle = handle
+    def __init__(self, *args: Any, **kwargs: Any) -> None:
+        warnings.warn("Please use `QuantileDMatrix` instead.", FutureWarning)
+        super().__init__(*args, **kwargs)
```

```json
{
  "old_file": "xgboost.core.DeviceQuantileDMatrix/Vi-1_v1.6.2.py",
  "new_file": "xgboost.core.DeviceQuantileDMatrix/Vi_v1.7.0.py",
  "lines_added": 4,
  "lines_removed": 90
}
```
