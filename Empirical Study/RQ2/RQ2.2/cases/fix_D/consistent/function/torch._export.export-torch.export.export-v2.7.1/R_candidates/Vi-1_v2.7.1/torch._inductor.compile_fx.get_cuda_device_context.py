def get_cuda_device_context(gm: torch.fx.GraphModule) -> AbstractContextManager[None]:
    """
    Returns a cuda device context manager if there is a single device in the graph
    """
    if not torch.cuda.is_available():
        return contextlib.nullcontext()

    placeholder_nodes = gm.graph.find_nodes(op="placeholder")
    input_devices: OrderedSet[torch.device] = OrderedSet(
        node.meta["val"].device
        for node in placeholder_nodes
        if isinstance(node.meta.get("val"), torch.Tensor)
    )

    out_devices: OrderedSet[torch.device] = OrderedSet(
        arg.meta["val"].device
        for arg in output_node(gm).args[0]  # type: ignore[union-attr]
        if isinstance(arg, fx.Node) and isinstance(arg.meta.get("val"), torch.Tensor)
    )
    cuda_devices: OrderedSet[torch.device] = OrderedSet(
        device for device in (input_devices | out_devices) if device.type == "cuda"
    )

    return (
        torch.cuda.device(next(iter(cuda_devices)))  # type: ignore[return-value]
        if len(cuda_devices) == 1
        else contextlib.nullcontext()
    )
