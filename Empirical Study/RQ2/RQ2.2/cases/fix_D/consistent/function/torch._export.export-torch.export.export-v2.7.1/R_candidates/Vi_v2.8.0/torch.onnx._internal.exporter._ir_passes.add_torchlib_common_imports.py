def add_torchlib_common_imports(
    model: ir.Model, opset_version: int = _constants.TORCHLIB_OPSET
) -> None:
    """Hack to add torchlib common imports to the model."""

    try:
        # TODO(justinchuby): Remove this hack and improved onnxscript
        from onnxscript.function_libs.torch_lib.ops import common as common_ops

        model.opset_imports["pkg.onnxscript.torch_lib.common"] = 1
        rank_func = ir.serde.deserialize_function(common_ops.Rank.to_function_proto())
        rank_func.opset_imports[""] = opset_version
        is_scalar_func = ir.serde.deserialize_function(
            common_ops.IsScalar.to_function_proto()
        )
        is_scalar_func.opset_imports[""] = opset_version
        model.functions[rank_func.identifier()] = rank_func
        model.functions[is_scalar_func.identifier()] = is_scalar_func
    except Exception:
        logger.exception("Failed to add torchlib common imports to the model.")
