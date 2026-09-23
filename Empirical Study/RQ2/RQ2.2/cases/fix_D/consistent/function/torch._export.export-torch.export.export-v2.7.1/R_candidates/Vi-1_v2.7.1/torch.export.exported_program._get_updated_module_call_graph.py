def _get_updated_module_call_graph(
    gm: torch.fx.GraphModule,
    old_module_call_graph: list[ModuleCallEntry],
):
    new_module_call_graph = copy.deepcopy(old_module_call_graph)

    # use node-level provenance metadata to create a map
    # from old node names to new node names
    provenance: dict[str, str] = {}
    for node in gm.graph.nodes:
        if history := node.meta.get("from_node", []):
            provenance[history[-1].name] = node.name

    # map old names to new names in module call signatures
    for entry in new_module_call_graph:
        signature = entry.signature
        if signature is None:
            continue
        for x in [*signature.inputs, *signature.outputs]:
            x.name = provenance.get(x.name, x.name)

    return new_module_call_graph
