def export(
    f: Callable,
    args: Tuple[Any, ...],
    kwargs: Optional[Dict[str, Any]] = None,
    constraints: Optional[List[Constraint]] = None,
    *,
    strict: bool = True,
    preserve_module_call_signature: Tuple[str, ...] = (),
) -> ExportedProgram:

    if constraints is not None:
        warnings.warn(
            "Using `constraints` to specify dynamic shapes for export is DEPRECATED "
            "and will not be supported in the future. "
            "Please use `dynamic_shapes` instead (see docs on `torch.export.export`).",
            DeprecationWarning,
            stacklevel=2,
        )
    return _export(
        f,
        args,
        kwargs,
        constraints,
        strict=strict,
        preserve_module_call_signature=preserve_module_call_signature,
    )
