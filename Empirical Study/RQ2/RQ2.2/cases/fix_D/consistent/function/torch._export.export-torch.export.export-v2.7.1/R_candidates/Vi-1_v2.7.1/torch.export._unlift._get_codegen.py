def _get_codegen(
    in_spec: pytree.TreeSpec,
    out_spec: Optional[pytree.TreeSpec],
    forward_arg_names: Optional[list[str]] = None,
) -> _PyTreeCodeGen:
    """
    Create the codegen for the graph module based on the in/out specs
    """
    if forward_arg_names:
        names = forward_arg_names
    else:
        if (
            in_spec.type == tuple
            and in_spec.num_children == 2
            and in_spec.children_specs[0].type == tuple
            and in_spec.children_specs[1].type == dict
        ):
            # if in_spec contains the args (tuple) and kwargs (dict)
            names = [f"arg_{i}" for i in range(in_spec.children_specs[0].num_children)]
            # add kwarg names
            names.extend(in_spec.children_specs[1].context)
        else:
            names = [f"arg_{i}" for i in range(in_spec.num_children)]

    return _PyTreeCodeGen(
        _PyTreeInfo(
            names,
            in_spec,
            out_spec,
        )
    )
