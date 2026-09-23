def _process_export_inputs(mod, args, kwargs, dynamic_shapes):
    if not isinstance(args, tuple):
        raise UserError(
            UserErrorType.INVALID_INPUT,
            f"Expecting `args` to be a tuple of example positional inputs, got {type(args)}",
        )
    kwargs = kwargs if kwargs is not None else {}
    _, original_in_spec = pytree.tree_flatten((args, kwargs))

    if isinstance(dynamic_shapes, torch.export.AdditionalInputs):
        verify_additional_inputs = dynamic_shapes.verify
        dynamic_shapes = dynamic_shapes.dynamic_shapes(mod, args, kwargs)
    else:
        verify_additional_inputs = lambda ep: None  # noqa: E731
        if isinstance(dynamic_shapes, torch.export.ShapesCollection):
            dynamic_shapes = dynamic_shapes.dynamic_shapes(mod, args, kwargs)

    return args, kwargs, original_in_spec, dynamic_shapes, verify_additional_inputs
