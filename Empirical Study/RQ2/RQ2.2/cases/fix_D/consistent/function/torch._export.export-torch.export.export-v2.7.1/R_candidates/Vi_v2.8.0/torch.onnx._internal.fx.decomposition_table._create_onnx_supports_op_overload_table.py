def _create_onnx_supports_op_overload_table(
    registry,
) -> set[torch._ops.OperatorBase | Callable]:
    """
    Creates a set of OperatorBase and Callable objects that represent ONNX-supported PyTorch operations.

    Args:
        registry (OnnxRegistry): The ONNX registry for PyTorch.

    Returns:
        A collection of OperatorBase and Callable objects representing ONNX-supported PyTorch operations.
    """
    table: set[torch._ops.OperatorBase | Callable] = set()

    # Some ops in `torch.ops.aten` are not discoverable through `dir(torch.ops.aten)`,
    # but retrievable via explicit lookup.
    # https://github.com/pytorch/pytorch/issues/99681
    # This is a workaround to make sure we register ONNX symbolic functions for these.
    onnx_supported_aten_lookup_table = [
        k.split("::")[1].split(".")[0]
        for k in registry._all_registered_ops()
        if k.startswith("aten::")
    ]

    for op_namespace in (torch.ops.aten, torch.ops.prims):
        attr_names = dir(op_namespace)
        if op_namespace is torch.ops.aten:
            attr_names += onnx_supported_aten_lookup_table
        for attr_name in attr_names:
            if not hasattr(op_namespace, attr_name):
                # torchlib owns some attributes that are not aten ops.
                continue
            op_overload_packet = getattr(op_namespace, attr_name)
            if not isinstance(op_overload_packet, torch._ops.OpOverloadPacket):
                continue

            for overload_name in op_overload_packet.overloads():
                op_overload = getattr(op_overload_packet, overload_name)
                internal_op_name = registration.OpName.from_qualified_name(
                    qualified_name=op_overload.name()
                )
                # NOTE: If the overload is supported in registry or it's default overload is supported in registry,
                # we add it to the table.
                if registry.is_registered_op(
                    namespace=internal_op_name.namespace,
                    op_name=internal_op_name.op_name,
                    overload=internal_op_name.overload,
                ) or registry.is_registered_op(
                    namespace=internal_op_name.namespace,
                    op_name=internal_op_name.op_name,
                    overload=None,
                ):
                    # This line maps torch.ops.aten.add.Tensor, torch.ops.aten.add.Scalar, torch.ops.aten.add.out, etc
                    # to "aten::add". This means the exporter for "aten::add" is used for all overloads of "aten::add".
                    # This is applied to all ops under torch.ops.aten.
                    table.add(op_overload)
    return table
