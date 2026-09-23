def _deserialize_graph_module(
    forward, body: dict[Any, Any], graph_module_cls=None
) -> torch.nn.Module:
    """
    Deserialize a GraphModule given the dictionary of the original module,
    using the code to reconstruct the graph. We delete the actual graph before
    saving the dictionary so that changes to the in-memory graph format do not
    get serialized.
    """

    # Try to retrieve the forward source in a backward-compatible way
    _CodeOnlyModule.forward = forward

    tracer_cls = body.get("_tracer_cls")
    if tracer_cls is None:
        from ._symbolic_trace import Tracer

        tracer_cls = Tracer

    graphmodule_cls_name = body.get("_graphmodule_cls_name", "GraphModule")

    # This is a workaround for a mypy linter issue related to
    # passing base class as an argument - https://github.com/python/mypy/issues/5865.
    cls_tracer: Any = tracer_cls

    class KeepModules(cls_tracer):
        # we shouldn't trace into any of the submodules,
        # because they were not traced in the original GraphModule
        def is_leaf_module(self, _: torch.nn.Module, __: str) -> bool:
            return True

    com = _CodeOnlyModule(body)

    tracer_extras = body.get("_tracer_extras", {})
    graph = KeepModules().trace(com, **tracer_extras)

    # Manually set Tracer class on the reconstructed Graph, to avoid
    # referencing the private local subclass KeepModules.
    graph._tracer_cls = tracer_cls
    from ._lazy_graph_module import _make_graph_module

    gm = _make_graph_module(
        com, graph, class_name=graphmodule_cls_name, graph_module_cls=graph_module_cls
    )

    # The GraphModule constructor only retains attributes referenced by the graph.
    # In this case, our goal is return a GraphModule as close to identical as the one
    # put into the package. If any additional attributes were present in body,
    # we should keep them.
    for k, v in body.items():
        if not hasattr(gm, k):
            setattr(gm, k, v)
    return gm
