def make_constraints(
    fake_mode: FakeTensorMode,
    gm: torch.fx.GraphModule,
    combined_args: dict[str, Any],
    dynamic_shapes: Union[dict[str, Any], tuple[Any], list[Any], None],
    num_lifted_inputs: int,
):
    """
    Given a fake mode's shape env and user-specified dynamic shapes,
    return the resulting range constraints and equality constraints.

    Additional args:
        num_lifted_inputs: the number of non-user-input placeholder nodes in the graph
        (used only to enumerate the user-input nodes)
    """

    shape_env = fake_mode.shape_env
    assert shape_env is not None
    inline_constraints = gm.meta.get("inline_constraints", [])
    range_constraints = {
        symbol: inline_constraints[symbol] for symbol in inline_constraints
    }
    if not dynamic_shapes:
        return range_constraints

    # clean up dynamic markers from tensors
    for arg in pytree.tree_flatten(combined_args)[0]:
        if isinstance(arg, torch.Tensor):
            _clean_dynamic_markers(arg)

    # get individual dynamic shapes spec for each input
    if not isinstance(dynamic_shapes, dict):
        assert isinstance(dynamic_shapes, (tuple, list))
        combined_args = type(dynamic_shapes)(combined_args.values())  # type: ignore[assignment, misc]
    flat_dynamic_shapes = _flatten_dynamic_shapes(combined_args, dynamic_shapes)

    # check number of shapes vs. number of inputs
    num_placeholders = [node.op == "placeholder" for node in gm.graph.nodes].count(True)
    assert len(flat_dynamic_shapes) == num_placeholders - num_lifted_inputs

    input_dims = defaultdict(list)
    free_symbols = set()
    for input_index, node in enumerate(gm.graph.nodes):
        if input_index < num_lifted_inputs or node.op != "placeholder":
            continue
        if _is_constant_argument(node.meta["val"]) or isinstance(
            node.meta["val"], CustomObjArgument
        ):
            continue
        shape_spec = flat_dynamic_shapes[input_index - num_lifted_inputs]
        for i, d in enumerate(node.meta["val"].shape):
            if isinstance(d, torch.SymInt) and not d.node.expr.is_number:
                # Look up the range constraint for the symbol corresponding to this shape dimension
                # and store it indexed by the symbolic expression corresponding to it.
                # NOTE(avik): Use node._expr instead of node.expr for the lookup here because
                # we want the symbol, not its replacement, which could be an expression. Maybe
                # there's a better way to do this, e.g., by (re)computing value ranges for expressions?
                dim = shape_spec[i] if shape_spec else None
                if dim is None or isinstance(dim, _DimHint):
                    range_constraints[d.node.expr] = shape_env.var_to_range[
                        d.node._expr
                    ]
                else:
                    range_constraints[d.node.expr] = ValueRanges(
                        lower=dim.min, upper=dim.max
                    )
                input_dims[d.node.expr].append(InputDim(input_name=node.name, dim=i))
                free_symbols.update(d.node.expr.free_symbols)

    for symbol in free_symbols:
        if symbol not in range_constraints:
            # Placeholders can have symbolic shapes that are derived expressions.
            # The above code will record direct range constraints for them
            # so that we can do runtime assertions. In addition, for serde checks
            # we want to record range constraints for their root symbols.
            range_constraints[symbol] = shape_env.var_to_range[symbol]

    return range_constraints
