def fakify(
    mode: FakeTensorMode,
    kp: KeyPath,
    t: Any,
    t_constraints: dict[int, dict[int, Constraint]],
    sources: dict[tuple[int, int], list[Source]],
):
    source = key_path_to_source(kp)
    if _is_constant_argument(t) or isinstance(t, (torch.ScriptObject, torch.nn.Module)):
        return t

    if not isinstance(t, torch.Tensor):
        raise ValueError(
            f"Unsupported input type {type(t)}. "
            "Export only supports pytree containers of basic types (Tensor, int, float, ...) as input. "
            "To register a custom dataclass, use torch.export.register_dataclass. "
            "To register a custom container type, use torch.utils._pytree.register_pytree_node. "
            "To register a constant input, use torch.utils._pytree.register_constant"
        )
    n_dims = len(t.shape)
    dynamic_sizes = []
    constraint_sizes = [None] * n_dims
    for i in range(n_dims):
        if i in getattr(t, "_dynamo_weak_dynamic_indices", {}):
            dynamic_sizes.append(DimDynamic.DYNAMIC)
        elif i in getattr(t, "_dynamo_dynamic_indices", {}):
            # bit annoying, but we need to replicate process in _dynamo/variables/builder.py
            # where a RelaxedUnspecConstraint is created for Dim.DYNAMIC, so constraint violations
            # are raised when specializing.
            dynamic_sizes.append(DimDynamic.DYNAMIC)
            constraint_sizes[i] = RelaxedUnspecConstraint(warn_only=False)  # type: ignore[call-overload]
        else:
            dynamic_sizes.append(DimDynamic.STATIC)
    symbolic_context = StatelessSymbolicContext(
        dynamic_sizes=dynamic_sizes,
        constraint_sizes=constraint_sizes,  # type: ignore[arg-type]
    )
    t_id = id(t)
    assert mode.shape_env is not None
    if t_id in t_constraints:
        for i, constraint in t_constraints[t_id].items():
            src = TensorPropertySource(base=source, prop=TensorProperty.SIZE, idx=i)
            sources[(t_id, i)].append(src)
            if isinstance(constraint, _RelaxedConstraint):
                continue
            symbolic_context.constraint_sizes[i] = constraint.constraint_range
            mode.shape_env.source_name_to_debug_name[src.name()] = constraint.name  # type: ignore[assignment]
    fake = mode.from_tensor(t, source=source, symbolic_context=symbolic_context)
    mode.shape_env.tracked_fakes.append(TrackedFake(fake, source, symbolic_context))  # type: ignore[union-attr]
    return fake
