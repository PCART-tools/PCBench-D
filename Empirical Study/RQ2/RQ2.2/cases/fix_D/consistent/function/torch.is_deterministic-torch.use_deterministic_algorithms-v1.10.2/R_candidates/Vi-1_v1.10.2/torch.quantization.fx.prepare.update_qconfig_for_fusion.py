def update_qconfig_for_fusion(
    model: GraphModule,
    qconfig_dict: Any,
) -> Any:
    """
    Update the qconfig_dict to account for fused modules such as LinearReLU.
    """
    object_type_dict = qconfig_dict.get("object_type", None)
    if object_type_dict is None:
        return qconfig_dict

    modules = dict(model.named_modules())

    for node in model.graph.nodes:
        if node.op == 'call_module':
            module_type = type(modules[str(node.target)])
            if module_type not in list(DEFAULT_OP_LIST_TO_FUSER_METHOD.values()):
                continue

            for ops, fuser in DEFAULT_OP_LIST_TO_FUSER_METHOD.items():
                if module_type == fuser:
                    fused_qconfig = object_type_dict.get(ops[0], None)

                    # Raise an error if the modules in the fused module have
                    # different qconfigs specified in the qconfig_dict
                    for op in ops:
                        if not qconfig_equals(object_type_dict.get(op, None), fused_qconfig):
                            raise LookupError("During fusion, we need to specify the same " +
                                              f"qconfigs for both modules in {module_type}.")

                    if fused_qconfig is not None:
                        object_type_dict[module_type] = fused_qconfig

    return qconfig_dict
