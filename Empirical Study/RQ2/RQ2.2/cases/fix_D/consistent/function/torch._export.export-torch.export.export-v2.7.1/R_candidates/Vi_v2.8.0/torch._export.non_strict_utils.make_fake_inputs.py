def make_fake_inputs(
    nn_module,
    args,
    kwargs,
    dynamic_shapes,
    _is_torch_jit_trace=False,
    allow_complex_guards_as_runtime_asserts=False,
):
    """
    Given an nn module, example inputs, and constraints, return a new fake mode,
    fake inputs created in that mode whose dynamic shape dimensions are constrained
    by the given ranges, and sources for pairs of dynamic shape dimensions that are
    constrained to be equal.
    """
    # TODO(avik): refactor Dynamo to avoid duplication of the following code
    # between non-strict and strict.
    # Specifically, here (non-strict) we do the following pre-tracing steps:
    #   - Fakify inputs.
    #   - Process input shape equalities.
    # In strict, these steps are spread across multiple files:
    #   - output_graph.py fakifies inputs.
    #   - [post-tracing] guards.py processes input shape equalities.
    import torch._functorch.config as _config

    # Map ints to a wrapper structure to help us mark it as dynamic, if it is
    # dynamic. We will unwrap ints in fakify later.
    args, kwargs = pytree.tree_map_only(int, lambda a: _IntWrapper(a), (args, kwargs))

    combined_args = _combine_args(nn_module, args, kwargs)
    _check_dynamic_shapes(combined_args, dynamic_shapes)
    constraints = _process_dynamic_shapes(combined_args, dynamic_shapes)
    t_constraints: dict[int, dict[int, Constraint]] = defaultdict(dict)
    for constraint in constraints:
        t_constraints[constraint.t_id][constraint.dim] = constraint

    context = torch._guards.TracingContext.try_get()
    if context is not None:
        # This occurs when we are exporting within dynamo. There already exists
        # a toplevel TracingContext with a fake mode, so we do not want to
        # create another fake mode.
        fake_mode = context.fake_mode
    elif not _is_torch_jit_trace:
        if isinstance(nn_module.forward, functools.partial):
            # functools handles nesting by itself, no need to recurse
            code = nn_module.forward.func.__code__
        else:
            code = nn_module.forward.__code__
        co_fields = {
            "co_name": code.co_name,
            "co_filename": code.co_filename,
            "co_firstlineno": code.co_firstlineno,
        }
        with _config.patch(fake_tensor_allow_unsafe_data_ptr_access=False):
            fake_mode = FakeTensorMode(
                shape_env=ShapeEnv(
                    tracked_fakes=[],
                    co_fields=co_fields,
                    prefer_deferred_runtime_asserts_over_guards=True,
                    allow_complex_guards_as_runtime_asserts=allow_complex_guards_as_runtime_asserts,
                    trace_asserts=True,
                ),
                allow_non_fake_inputs=True,
                export=True,
            )
    else:
        with _config.patch(fake_tensor_allow_unsafe_data_ptr_access=False):
            fake_mode = FakeTensorMode(
                shape_env=ShapeEnv(
                    tracked_fakes=[],
                    prefer_deferred_runtime_asserts_over_guards=True,
                    allow_complex_guards_as_runtime_asserts=allow_complex_guards_as_runtime_asserts,
                    trace_asserts=True,
                ),
                allow_non_fake_inputs=True,
            )
    if fake_mode.shape_env is None or fake_mode.shape_env.tracked_fakes is None:
        raise ValueError(
            "Detected fake_mode does not have a shape_env with tracked fakes. "
            "If you constructed the module under a FakeTensorMode, "
            "please initialize it like: FakeTensorMode(shape_env=ShapeEnv(tracked_fakes=[]))"
        )

    with fake_mode:
        # FIXME(ycao) ScriptMethod doesn't have signature, I am using an empty one to unblock
        if not _is_torch_jit_trace:
            original_signature = inspect.signature(nn_module.forward)
        else:
            original_signature = None
        sources: dict[tuple[int, int], list[Source]] = defaultdict(list)
        sourced_prefixes = make_sourced_prefixes(nn_module, args, kwargs)
        fake_args, fake_kwargs = tree_map_with_path(
            lambda kp, val: fakify(
                fake_mode,
                kp,
                val,
                t_constraints,
                sources,
                sourced_prefixes=sourced_prefixes,
            ),
            (args, kwargs),
        )

        names: dict[str, tuple[int, int]] = {}
        source_pairs: list[tuple[Source, Source]] = []
        derived_equalities: list[tuple[Source, Union[Source, Symbol], Callable]] = []
        phantom_symbols: dict[str, Symbol] = {}
        relaxed_sources: set[Source] = set()
        for constraint in constraints:
            torch.export.dynamic_shapes._process_equalities(
                constraint,
                lambda t_id, dim: sources[(t_id, dim)],
                fake_mode.shape_env,
                names,
                source_pairs,
                derived_equalities,
                phantom_symbols,
                relaxed_sources,
            )

        equalities_inputs = EqualityConstraint(
            source_pairs=source_pairs,
            derived_equalities=derived_equalities,
            phantom_symbols=list(phantom_symbols.values()),
            relaxed_sources=relaxed_sources,
            warn_only=False,
        )
        return (
            fake_mode,
            fake_args,
            fake_kwargs,
            equalities_inputs,
            original_signature,
            dynamic_shapes,
        )
