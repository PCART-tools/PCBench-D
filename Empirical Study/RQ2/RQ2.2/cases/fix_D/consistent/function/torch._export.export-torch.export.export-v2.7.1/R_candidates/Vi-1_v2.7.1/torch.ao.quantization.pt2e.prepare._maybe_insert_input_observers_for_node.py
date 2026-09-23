def _maybe_insert_input_observers_for_node(
    node: Node,
    qconfig: QConfigAny,
    model: torch.nn.Module,
    named_modules: dict[str, torch.nn.Module],
    obs_or_fq_map: dict[EdgeOrNode, ObserverOrFakeQuantize],
    is_qat: bool,
) -> None:
    """
    If needed, inserts observers to the input args and kwargs of `node`.
    Note: modifies `node` inplace.

    For example, if cur_node needs an observer after prev_node, we change from

      prev_node -> cur_node

    To

      prev_node -> obs -> cur_node

    """
    # Look through every input arg.  If that arg's target dtype does not
    # match the current node's target dtype, insert an observer.
    new_args = []
    for arg in node.args:
        new_arg = _maybe_insert_input_observer_for_arg_or_kwarg(
            node,
            arg,
            qconfig,
            model,
            named_modules,
            obs_or_fq_map,
            is_qat,
        )
        new_args.append(new_arg)

    # Clone has a memory_format kwarg, zeros_like has a pin_memory kwarg, and
    # gelu has a has an approximate kwarg that persist in exported graph.
    # This is just a work around for these.
    assert (
        node.target == torch.ops.aten.clone.default
        or node.target == torch.ops.aten.zeros_like.default
        or node.target == torch.ops.aten.gelu.default
        or len(node.kwargs) == 0
    ), " expecting kwargs for aten op IR to be empty"

    # assign the new args to the node, inplace
    node.args = tuple(new_args)
