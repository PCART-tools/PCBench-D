def reorder_kwargs(user_kwargs: dict[str, Any], spec: TreeSpec) -> dict[str, Any]:
    """Reorder user-provided kwargs to match the order in `spec`. `spec` is
    expected to be the in_spec of an exported program, i.e. the spec that
    results from flattening `(args, kwargs)`.

    We need this to provide consistent input ordering, such so that users can
    pass in foo(a=a, b=b) OR foo(b=b, a=a) and receive the same result.
    """
    # Make sure that the spec is actually shaped like (args, kwargs)
    assert spec.type is tuple
    assert spec.num_children == 2
    kwargs_spec = spec.children_specs[1]
    assert kwargs_spec.type is dict

    if set(user_kwargs) != set(kwargs_spec.context):
        raise ValueError(
            f"Ran into a kwarg keyword mismatch: "
            f"Got the following keywords {list(user_kwargs)} but expected {kwargs_spec.context}"
        )

    reordered_kwargs = {}
    for kw in kwargs_spec.context:
        reordered_kwargs[kw] = user_kwargs[kw]

    return reordered_kwargs
