def get_normalized_kwargs(
    node: torch.fx.Node, arg_replacement_tuples: ArgReplacementTuplesType
):
    new_kwargs = {}
    final_arg_is_varg = False
    for i, replacement_tuple in enumerate(arg_replacement_tuples):
        orig_kwargs_names, new_kwarg_name, is_optional = replacement_tuple

        # Check if this is a varg and if so break/process the rest outside the loop.
        if len(orig_kwargs_names) == 1 and orig_kwargs_names[0] == "*":
            assert i == len(arg_replacement_tuples) - 1
            final_arg_is_varg = True
            break

        # If nothing is found in node.kwargs it means the kwarg is in node.arg
        # or it's optional. In this case, we set orig_kwargs_name to None.
        assert isinstance(orig_kwargs_names, tuple)
        orig_kwargs_name = next(
            (key for key in orig_kwargs_names if key in node.kwargs),
            None,
        )

        # If can't find in node.kwargs then it should be in the i index
        # of node.args.
        if orig_kwargs_name is None:
            if i < len(node.args):
                new_kwargs[new_kwarg_name] = node.args[i]
            else:
                # Verify the arg we're trying to normalize was optional.
                assert is_optional, f"Cannot normalize {orig_kwargs_names} to {new_kwarg_name} for {node.name}"
        else:
            new_kwargs[new_kwarg_name] = node.kwargs[orig_kwargs_name]

    # If using var args then process the rest of the args now.
    if final_arg_is_varg:
        var_arg_idx = len(arg_replacement_tuples) - 1
        new_kwarg_name = arg_replacement_tuples[var_arg_idx][1]
        rest_of_args = []
        for i in range(var_arg_idx, len(node.args)):
            rest_of_args.append(node.args[i])
        new_kwargs[new_kwarg_name] = rest_of_args

    return new_kwargs
