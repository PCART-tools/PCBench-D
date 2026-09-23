def _outline_submodules(orig_graph: torch.fx.Graph, root_module: UnflattenedModule):
    seen_nodes: dict[str, torch.fx.Node] = {}
    seen_modules: dict[int, list[_SubmoduleEntry]] = defaultdict(list)
    seen_attrs: dict[str, set[str]] = defaultdict(set)
    created_modules: dict[str, torch.nn.Module] = {}
    _ModuleFrame(
        orig_graph,
        tuple(orig_graph.nodes),
        seen_nodes,
        seen_modules,
        seen_attrs,
        created_modules,
        None,
        [("", None, 0)],
        "",
        {
            entry.fqn: entry.signature
            for entry in root_module.module_call_graph
            if entry.signature
        },
        module=root_module,
    ).run_outer()
    return seen_modules, seen_attrs
