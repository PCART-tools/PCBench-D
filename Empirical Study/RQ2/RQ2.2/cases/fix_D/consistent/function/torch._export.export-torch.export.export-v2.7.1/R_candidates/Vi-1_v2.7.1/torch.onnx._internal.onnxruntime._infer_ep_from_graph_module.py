def _infer_ep_from_graph_module(graph_module: torch.fx.GraphModule) -> tuple[str, ...]:
    """Return the all valid devices (i.e., GPU or CPU) among outputs of this torch.fx.GraphModule."""
    flattened_output_args, _ = _pytree.tree_flatten(
        _extract_graph_module_outputs(graph_module)
    )
    # Output arguments with example value (type: torch.Tensor) in the `graph_module`.
    selected_output_args = [
        output_arg.meta["val"]
        for output_arg in flattened_output_args
        # output_arg must have tensor for its device information.
        # Otherwise, skip it.
        if (hasattr(output_arg, "meta") and "val" in output_arg.meta)
    ]
    return _infer_ep_from_device(*selected_output_args)
