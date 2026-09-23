def is_onnxrt_backend_supported() -> bool:
    """Returns ``True`` if ONNX Runtime dependencies are installed and usable
    to support TorchDynamo backend integration; ``False`` otherwise.

    Example::

        # xdoctest: +REQUIRES(env:TORCH_DOCTEST_ONNX)
        >>> import torch
        >>> if torch.onnx.is_onnxrt_backend_supported():
        ...     @torch.compile(backend="onnxrt")
        ...     def f(x):
        ...             return x * x
        ...     print(f(torch.randn(10)))
        ... else:
        ...     print("pip install onnx onnxscript onnxruntime")
        ...
    """
    global _SUPPORT_ONNXRT

    if _SUPPORT_ONNXRT is None:
        # `onnxruntime` might import a lot of other runtime packages,
        # e.g. apex, deepspeed, transformers.
        # So lazy-importing onnxruntime to avoid possible circular import.
        try:
            importlib.import_module("onnxruntime")
            importlib.import_module("onnxruntime.capi._pybind_state")

            # This is not use directly in DORT but needed by underlying exporter,
            # so we still need to check if it exists.
            importlib.import_module("onnxscript")

            import torch.onnx  # noqa: F401
            import torch.onnx._internal  # noqa: F401
            import torch.onnx._internal._exporter_legacy  # noqa: F401
            import torch.onnx._internal.diagnostics  # noqa: F401
            from torch.onnx._internal.fx import (  # noqa: F401
                decomposition_table,
                fx_onnx_interpreter,
                passes,
                type_utils,
            )

            _SUPPORT_ONNXRT = True
        except ImportError:
            _SUPPORT_ONNXRT = False

    return _SUPPORT_ONNXRT
