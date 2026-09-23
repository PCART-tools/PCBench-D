def remove_duplicate_output_args(
    top_level: fx.GraphModule,
    target_subnets: t.Collection[str]
) -> t.Mapping[str, "RemoveDuplicateResult"]:
    """Removes duplicate output args.

    This pass removes duplicate output args from the target subnets and fixes
    their uses in the top level module where the subnets are called. This pass
    must be called after acc split on the top-level net and subsequent calls to
    the acc trace on the subnets.

    This pass will change both the subnets and top level module.

    Returns:
        a mapping of the target subnet name to its dedupcate result
    """

    processed_subnets = {}
    for node in top_level.graph.nodes:  # type: fx.Node
        if node.op == "call_module" and node.name in target_subnets:
            assert isinstance(node.target, str)
            sub_gm = top_level.get_submodule(node.target)
            assert isinstance(sub_gm, fx.GraphModule)

            replace_res = _remove_duplicate_output_args(sub_gm)
            processed_subnets[node.name] = replace_res
            if replace_res.replacement_map is None:
                continue
            sub_gm.recompile()

            needs_recompile = False
            # iterate on the copy since we will be changing elements of node.users
            for user in list(node.users):
                idx = _ensure_proper_output_use(user, node)
                idx_new = replace_res.replacement_map[idx]
                if idx_new != idx:
                    user.args = (user.args[0], idx_new)
                    needs_recompile = True

            if needs_recompile:
                top_level.recompile()
    return processed_subnets
