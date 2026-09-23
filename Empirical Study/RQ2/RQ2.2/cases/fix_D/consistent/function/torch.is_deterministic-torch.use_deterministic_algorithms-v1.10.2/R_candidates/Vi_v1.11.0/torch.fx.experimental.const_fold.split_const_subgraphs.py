def split_const_subgraphs(
    module: Union[torch.nn.Module, torch.fx.GraphModule],
    skip_folding_node_fn: Optional[Callable[[torch.fx.Node], bool]] = None
) -> FoldedGraphModule:
    """
    Looks through `module` for any nodes that have all constant attribute inputs
    and separates them out into their own constant subgraph, and returns a
    FoldedGraphModule which runs that constant subgraph on the first run to set
    attributes on the module prior to running the non-constant portion of the
    graph.
    """
    if not isinstance(module, torch.fx.GraphModule):
        mod_traced = torch.fx.symbolic_trace(module)
    else:
        mod_traced = module

    # Build up a list of const_nodes, defined as nodes that are themselves
    # get_attrs, or have all get_attr or other constant node inputs.
    const_nodes: Set[torch.fx.Node] = set()
    found_const_folding = False
    for node in mod_traced.graph.nodes:
        # Skip over placeholders/outputs because they can't be const folded and
        # we don't want to add tags to them.
        if node.op in {"placeholder", "output"}:
            continue

        # If the node itself is constant, or all of its inputs are constant,
        # then tag it as constant.
        if node.op != "get_attr" and not set(node.all_input_nodes).issubset(const_nodes):
            continue

        # If provided skip folding function says to skip, then skip.
        if skip_folding_node_fn and skip_folding_node_fn(node):
            continue

        # Must be a constant foldable node at this point.
        const_nodes.add(node)
        if node.op != "get_attr":
            found_const_folding = True

    # If we did not find any const folding then return early without a const fold subgraph.
    if not found_const_folding:
        return FoldedGraphModule(mod_traced, mod_traced.graph)

    # Partition the module into two: submod_0 for constant folding subgraph, and
    # submod_1 for the rest.
    def mod_partition(node: torch.fx.Node):
        return 0 if node in const_nodes else 1

    split = split_module(mod_traced, module, mod_partition)

    const_gm, non_const_gm = split.submod_0, split.submod_1
    const_mod_name, non_const_mod_name = "submod_0", "submod_1"

    # The module that a call_module node refers to gets copied to submodules during split.
    # The path to the module also gets inlined, i.e. mod.a.b -> mod_a_b. Here we need to
    # attach inlined modules to `split` as it's the owning module now.
    for node in non_const_gm.graph.nodes:
        if node.op == "call_module":
            setattr(split, node.target, getattr(non_const_gm, node.target))
    for node in const_gm.graph.nodes:
        if node.op == "call_module":
            setattr(split, node.target, getattr(const_gm, node.target))

    # split_module currently does not use get_attrs for attrs. Instead it passes
    # them in as args from the parent module, which used get_attrs. Here we set
    # them as get_attrs inside const_gm, allowing for running folding without
    # somehow a priori knowing the attrs that should be passed as args. We can
    # unconditionally do this for all placeholders because we know all
    # placeholders to const_gm must be constants accessible via get_attr.
    call_const_gm_args = None
    for node in split.graph.nodes:
        if node.op == "call_module":
            if node.target == const_mod_name:
                call_const_gm_args = node.args
                break
    assert call_const_gm_args is not None

    # Here we do the actual replacement of placeholders to get_attrs. Note that here we
    # set the const_gm.graph into a new root_const_gm with split as the root module,
    # because we are fetching attributes directly from the root module, instead of
    # fetching them from const_gm. Example: The const_gm must have some format like:
    # graph():
    #    %inp : [#users=1] = placeholder[target=const_inp]
    #    %add : [#users=1] = call_function[target=operator.add](args = (%inp, %inp), kwargs = {})
    #    return add
    # We replace that with the following, which does not have any placeholders:
    # graph():
    #    %inp_1 : [#users=1] = get_attr[target=const_inp]
    #    %add : [#users=1] = call_function[target=operator.add](args = (%inp_1, %inp_1), kwargs = {})
    #    return add
    root_const_gm = torch.fx.GraphModule(split, const_gm.graph)
    for node in root_const_gm.graph.nodes:
        if node.op == "output":
            multiple_outputs = isinstance(node.args[0], tuple)
            continue
        if node.op != "placeholder":
            continue
        in_node = next(n for n in call_const_gm_args if n.name == node.target)
        assert in_node.op == "get_attr"
        with root_const_gm.graph.inserting_before(node):
            new_node = root_const_gm.graph.get_attr(in_node.target)
        new_node.meta = node.meta.copy()
        node.replace_all_uses_with(new_node)
        root_const_gm.graph.erase_node(node)
    assert "multiple_outputs" in locals()

    # Now find the call to const_gm inside split, and replace it with a getattr to the
    # folded tensor(s) that result from constant folding. Note that we don't need to
    # worry about whether this is one or more tensors because the original graph
    # correctly uses getitem to extract individual tensors if there are multiple folded.
    fx_const_folded_attrs_name = acc_utils.get_unique_attr_name_in_module(
        split, "_FX_CONST_FOLDED_ATTRS"
    )
    setattr(
        split,
        fx_const_folded_attrs_name,
        torch.nn.ParameterList() if multiple_outputs else torch.nn.Parameter(),
    )
    for node in split.graph.nodes:
        if node.op == "call_module" and node.target == const_mod_name:
            with node.graph.inserting_before(node):
                folded_attrs = node.graph.get_attr(fx_const_folded_attrs_name)
            folded_attrs.meta = node.meta.copy()
            node.replace_all_uses_with(folded_attrs)
            break

    split.graph.eliminate_dead_code()

    # Finally, inline the non-constant submod into the split submod. This is so that the
    # original caller who may have passed in a graph module will get back out a graph
    # module whose graph is traced to the same granularity.
    _inline_module(split, non_const_mod_name)

    return FoldedGraphModule(
        split, split.graph, root_const_gm.graph, fx_const_folded_attrs_name
    )
