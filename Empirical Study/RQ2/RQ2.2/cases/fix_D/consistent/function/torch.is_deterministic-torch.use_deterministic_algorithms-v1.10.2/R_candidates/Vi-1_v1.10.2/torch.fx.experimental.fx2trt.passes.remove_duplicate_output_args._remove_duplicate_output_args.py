def _remove_duplicate_output_args(gm: fx.GraphModule) -> RemoveDuplicateResult:
    output_nodes = [n for n in gm.graph.nodes if n.op == "output"]
    assert len(output_nodes) == 1, \
           f"Expecting exactly one `output` node, but got {len(output_nodes)}"

    changed = False
    # arg node name to its index in the new output args tuple
    name_to_idx: t.Dict[str, int] = {}
    output_node = output_nodes[0]

    # Output op only uses its `args[0]`, and it does not have `kwargs`.
    # https://pytorch.org/docs/stable/fx.html#torch.fx.Node
    args: t.Sequence[t.Any] = output_node.args[0]

    # Only concern outselves to the case where the args is an iterable of fx.Node.
    # Other return cases (e.g., a single value) is possible and we don't handle
    # that in this pass.
    if not (isinstance(args, t.Iterable) and all(isinstance(a, fx.Node) for a in args)):
        return RemoveDuplicateResult(replacement_map=None, module=gm)

    # Map old index of the arg node to the remaining node's idx,
    # initialized to `i => i`
    replacement_map: t.List[int] = list(range(len(args)))
    args_new = []
    for idx, a in enumerate(args):
        assert isinstance(a, fx.Node), \
               f"Expecting fx.Node instance, but got: {type(a)}"

        if a.name not in name_to_idx:
            args_new.append(a)
            name_to_idx[a.name] = len(args_new) - 1
        else:
            changed = True
            _LOGGER.warning(
                f"Replaced duplicate output arg '{a.name}': "
                f"{idx} -> {name_to_idx[a.name]}"
            )
        replacement_map[idx] = name_to_idx[a.name]

    output_node.args = (tuple(args_new),)
    if changed:
        gm.recompile()
    return RemoveDuplicateResult(replacement_map, module=gm)
