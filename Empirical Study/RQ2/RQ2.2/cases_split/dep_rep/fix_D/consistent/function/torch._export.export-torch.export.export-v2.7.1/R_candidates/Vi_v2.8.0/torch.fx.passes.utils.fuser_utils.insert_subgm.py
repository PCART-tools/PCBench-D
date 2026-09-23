@compatibility(is_backward_compatible=False)
def insert_subgm(
    gm: GraphModule,
    sub_gm: GraphModule,
    orig_inputs: tuple[Node, ...],
    orig_outputs: tuple[Node, ...],
) -> GraphModule:
    # add sub_gm into gm
    submodule_name = sub_gm.__class__.__name__
    gm.add_submodule(submodule_name, sub_gm)

    # Create a call_module node in main graph.
    module_node = gm.graph.call_module(submodule_name, args=orig_inputs, kwargs=None)

    output_node = sub_gm.graph.output_node()
    if len(orig_outputs) == 1 and not isinstance(output_node.args[0], tuple):
        # main_remapping[comp.orig_outputs[0]] = module_node
        orig_outputs[0].replace_all_uses_with(module_node, propagate_meta=True)
    else:
        for i, orig_output in enumerate(orig_outputs):
            # Use Proxy to record getitem access.
            proxy_out = torch.fx.Proxy(module_node)[i].node  # type: ignore[index]
            orig_output.replace_all_uses_with(proxy_out, propagate_meta=True)

        module_node.meta["val"] = tuple(
            orig_output.meta.get("val", None) for orig_output in orig_outputs
        )
    return gm
