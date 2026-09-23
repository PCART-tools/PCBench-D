def symbolic_trace(
    root: Union[torch.nn.Module, Callable[..., Any]],
    meta_args: Optional[dict[str, torch.Tensor]] = None,
    concrete_args: Optional[dict[str, Any]] = None,
) -> torch.fx.GraphModule:
    tracer = MetaTracer()
    graph = tracer.trace(root, meta_args, concrete_args)  # type: ignore[arg-type]
    name = (
        root.__class__.__name__ if isinstance(root, torch.nn.Module) else root.__name__
    )
    gm = torch.fx.GraphModule(tracer.root, graph, name)
    return gm
