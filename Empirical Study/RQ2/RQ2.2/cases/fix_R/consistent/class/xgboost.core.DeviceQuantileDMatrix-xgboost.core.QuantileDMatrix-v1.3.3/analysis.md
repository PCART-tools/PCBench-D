# 一、突变情况分析

- **Total**: 85
- **替代API**: `xgboost.core.QuantileDMatrix`
- **10% 阈值**: 8.5

## Vi-1 (v1.3.3-v3.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 2 | 0.3215 |
| tokenBased | 24 | 0.2533 |

## Vi (v1.4.0-v3.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 1 | 0.7290 |
| tokenBased | 2 | 0.4675 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 2 | 1 | +1 | false |
| tokenBased | 24 | 2 | +22 | true |

```json
{
  "total": 85,
  "replacement_api": "xgboost.core.QuantileDMatrix",
  "threshold_10pct": 8.5,
  "vi_minus_1": {
    "mapBased": {
      "rank": 2,
      "score": 0.321515
    },
    "tokenBased": {
      "rank": 24,
      "score": 0.253333
    }
  },
  "vi": {
    "mapBased": {
      "rank": 1,
      "score": 0.728966
    },
    "tokenBased": {
      "rank": 2,
      "score": 0.467456
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 2,
      "vi_rank": 1,
      "delta": 1,
      "exceeds_10pct": false
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 24,
      "vi_rank": 2,
      "delta": 22,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `xgboost.core.DeviceQuantileDMatrix/Vi-1_v1.3.3.py`
- **new**: `xgboost.core.DeviceQuantileDMatrix/Vi_v1.4.0.py`
- **+83 / -38**

```diff
--- xgboost.core.DeviceQuantileDMatrix/Vi-1_v1.3.3.py
+++ xgboost.core.DeviceQuantileDMatrix/Vi_v1.4.0.py
@@ -1,54 +1,99 @@
 class DeviceQuantileDMatrix(DMatrix):
     
 
-    def __init__(self, data, label=None, weight=None,
-                 base_margin=None,
-                 missing=None,
-                 silent=False,
-                 feature_names=None,
-                 feature_types=None,
-                 nthread=None, max_bin=256):
+    @_deprecate_positional_args
+    def __init__(
+        self,
+        data,
+        label=None,
+        *,
+        weight=None,
+        base_margin=None,
+        missing=None,
+        silent=False,
+        feature_names=None,
+        feature_types=None,
+        nthread: Optional[int] = None,
+        max_bin: int = 256,
+        group=None,
+        qid=None,
+        label_lower_bound=None,
+        label_upper_bound=None,
+        feature_weights=None,
+        enable_categorical: bool = False,
+    ):
         self.max_bin = max_bin
         self.missing = missing if missing is not None else np.nan
         self.nthread = nthread if nthread is not None else 1
+        self._silent = silent
 
         if isinstance(data, ctypes.c_void_p):
             self.handle = data
             return
-        from .data import init_device_quantile_dmatrix
-        handle, feature_names, feature_types = init_device_quantile_dmatrix(
-            data, missing=self.missing, threads=self.nthread,
-            max_bin=self.max_bin,
-            label=label, weight=weight,
+
+        if enable_categorical:
+            raise NotImplementedError(
+                'categorical support is not enabled on DeviceQuantileDMatrix.'
+            )
+        if qid is not None and group is not None:
+            raise ValueError(
+                'Only one of the eval_qid or eval_group for each evaluation '
+                'dataset should be provided.'
+            )
+
+        self._init(
+            data,
+            label=label,
+            weight=weight,
             base_margin=base_margin,
-            group=None,
-            label_lower_bound=None,
-            label_upper_bound=None,
+            group=group,
+            qid=qid,
+            label_lower_bound=label_lower_bound,
+            label_upper_bound=label_upper_bound,
+            feature_weights=feature_weights,
             feature_names=feature_names,
-            feature_types=feature_types)
-        self.handle = handle
-
-        self.feature_names = feature_names
-        self.feature_types = feature_types
-
-    def _set_data_from_cuda_interface(self, data):
-        
-        interface = data.__cuda_array_interface__
-        interface_str = bytes(json.dumps(interface, indent=2), 'utf-8')
-        _check_call(
-            _LIB.XGDeviceQuantileDMatrixSetDataCudaArrayInterface(
-                self.handle,
-                interface_str
-            )
+            feature_types=feature_types,
         )
 
-    def _set_data_from_cuda_columnar(self, data):
-        
-        from .data import _cudf_array_interfaces
-        interfaces_str = _cudf_array_interfaces(data)
-        _check_call(
-            _LIB.XGDeviceQuantileDMatrixSetDataCudaColumnar(
-                self.handle,
-                interfaces_str
+    def _init(self, data, feature_names, feature_types, **meta):
+        from .data import (
+            _is_dlpack,
+            _transform_dlpack,
+            _is_iter,
+            SingleBatchInternalIter,
+        )
+
+        if _is_dlpack(data):
+
+
+            data = _transform_dlpack(data)
+        if _is_iter(data):
+            it = data
+        else:
+            it = SingleBatchInternalIter(
+                data, **meta, feature_names=feature_names, feature_types=feature_types
             )
+
+        reset_callback = ctypes.CFUNCTYPE(None, ctypes.c_void_p)(it.reset_wrapper)
+        next_callback = ctypes.CFUNCTYPE(
+            ctypes.c_int,
+            ctypes.c_void_p,
+        )(it.next_wrapper)
+        handle = ctypes.c_void_p()
+        ret = _LIB.XGDeviceQuantileDMatrixCreateFromCallback(
+            None,
+            it.proxy.handle,
+            reset_callback,
+            next_callback,
+            ctypes.c_float(self.missing),
+            ctypes.c_int(self.nthread),
+            ctypes.c_int(self.max_bin),
+            ctypes.byref(handle),
         )
+        if it.exception is not None:
+
+
+            raise it.exception
+
+        _check_call(ret)
+        self.handle = handle
```

```json
{
  "old_file": "xgboost.core.DeviceQuantileDMatrix/Vi-1_v1.3.3.py",
  "new_file": "xgboost.core.DeviceQuantileDMatrix/Vi_v1.4.0.py",
  "lines_added": 83,
  "lines_removed": 38
}
```
