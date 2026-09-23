def extract_results_from_loggers(
    model: GraphModule,
) -> dict[int, tuple[Optional[str], object, list[object]]]:
    """For a given model, extract the tensors stats and related information for each debug handle.
    The reason we have a list of object, instead of Tensor is because the output of node may not be
    a Tensor, it could be (nested) list, tuple or dict as well.

    Returns:
        A dict is keyed by the debug_handle id and the values are a list of object recorded
        in loggers

    """
    # Results maps debug handle to a tensor list for each model being compared.
    handles: dict[int, tuple[Optional[str], object, list[object]]] = {}
    for _name, module in model.named_children():
        if isinstance(module, OutputLogger) and len(module.stats) > 0:
            handles[module.debug_handle] = (
                module.node_name,
                module.nn_module_stack,
                module.stats,
            )

    return handles
