def create_onnx_friendly_decomposition_table(
    registry,
) -> dict[torch._ops.OperatorBase, Callable]:
    """
    This function creates a dictionary of op overloads and their decomposition functions
    for ops that do not have ONNX symbolic functions. If an op already has an ONNX symbolic function,
    its decomposition function is excluded from the table. The decomposition table is a subset of PyTorch's
    built-in aten-to-aten decomposition.

    Args:
        registry: The ONNX registry for PyTorch.

    Returns:
        Dict[torch._ops.OperatorBase, Callable]: A dictionary that maps op overloads to their corresponding
        decomposition functions.
    """
    decomposition_table: dict[torch._ops.OperatorBase, Callable] = {}
    # Dictionary that maps torch.ops.aten.* to exporter look up key; e.g.,
    # _OP_OVERLOAD_TO_EXPORTER_KEY_TABLE[torch.add.Tensor] is "aten::add".
    _ONNX_SUPPORT_OP_OVERLOADS = _create_onnx_supports_op_overload_table(registry)

    # NOTE: If we import torch._decomp, we will get RuntimeError: Only a single
    # TORCH_LIBRARY can be used to register the namespace nvprims; please put all of your
    # definitions in a single TORCH_LIBRARY block.
    for op_overload, decomp_fn in torch._decomp.decomposition_table.items():
        # Skip decomposition into "prim::*" ops (defined in 'torch._refs'), because they
        # are not generally supported by ONNX.
        # Skip decomposition for op_overload as long as that op_overload has a corresponding ONNX
        # symbolic function.
        if (
            "torch._refs" in decomp_fn.__module__
            or op_overload in _ONNX_SUPPORT_OP_OVERLOADS
        ):
            continue
        decomposition_table[op_overload] = decomp_fn

    # NOTE: There are ops in core ATen and under torch._refs,
    # that are not decomposed to prim::ops. We need to pick them
    # back
    for op_overload, decomp_fn in torch._decomp.core_aten_decompositions().items():
        if op_overload in _ONNX_SUPPORT_OP_OVERLOADS:
            continue
        decomposition_table[op_overload] = decomp_fn
    return decomposition_table
