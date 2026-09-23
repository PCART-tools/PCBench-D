@deprecated(
    "torch.onnx.dynamo_export is deprecated since 2.7.0. Please use torch.onnx.export(..., dynamo=True) instead."
)
def dynamo_export(
    model: torch.nn.Module | Callable | torch.export.ExportedProgram,  # type: ignore[name-defined]
    /,
    *model_args,
    export_options: ExportOptions | None = None,
    **model_kwargs,
) -> ONNXProgram:
    """Export a torch.nn.Module to an ONNX graph.

    .. deprecated:: 2.7
        Please use ``torch.onnx.export(..., dynamo=True)`` instead.

    Args:
        model: The PyTorch model to be exported to ONNX.
        model_args: Positional inputs to ``model``.
        model_kwargs: Keyword inputs to ``model``.
        export_options: Options to influence the export to ONNX.

    Returns:
        An in-memory representation of the exported ONNX model.
    """

    import warnings

    from torch.onnx._internal.exporter import _compat
    from torch.utils import _pytree

    if isinstance(model, torch.export.ExportedProgram):
        return _compat.export_compat(
            model,  # type: ignore[arg-type]
            model_args,
            f=None,
            kwargs=model_kwargs,
            opset_version=18,
            external_data=True,
            export_params=True,
            fallback=True,
        )
    if export_options is not None:
        warnings.warn(
            "You are using an experimental ONNX export logic, which currently only supports dynamic shapes. "
            "For a more comprehensive set of export options, including advanced features, please consider using "
            "`torch.onnx.export(..., dynamo=True)`. ",
            category=DeprecationWarning,
        )

    if export_options is not None and export_options.dynamic_shapes:
        # Make all shapes dynamic if it's possible
        def _to_dynamic_shape(x):
            if isinstance(x, torch.Tensor):
                rank = len(x.shape)
                dynamic_shape = {}
                for i in range(rank):
                    dynamic_shape[i] = torch.export.Dim.AUTO
                return dynamic_shape
            else:
                return None

        # model_args could be nested
        dynamic_shapes = _pytree.tree_map(
            _to_dynamic_shape,
            model_args,
        )
    else:
        dynamic_shapes = None

    return _compat.export_compat(
        model,  # type: ignore[arg-type]
        model_args,
        f=None,
        kwargs=model_kwargs,
        dynamic_shapes=dynamic_shapes,
        opset_version=18,
        external_data=True,
        export_params=True,
        fallback=True,
    )
