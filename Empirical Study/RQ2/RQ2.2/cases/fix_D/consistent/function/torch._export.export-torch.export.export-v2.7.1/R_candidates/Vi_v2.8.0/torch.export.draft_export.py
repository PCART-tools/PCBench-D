def draft_export(
    mod: torch.nn.Module,
    args: tuple[Any, ...],
    kwargs: Optional[dict[str, Any]] = None,
    *,
    dynamic_shapes: Optional[Union[dict[str, Any], tuple[Any], list[Any]]] = None,
    preserve_module_call_signature: tuple[str, ...] = (),
    strict: bool = False,
) -> ExportedProgram:
    """
    A version of torch.export.export which is designed to consistently produce
    an ExportedProgram, even if there are potential soundness issues, and to
    generate a report listing the issues found.
    """
    from ._draft_export import draft_export

    return draft_export(
        mod=mod,
        args=args,
        kwargs=kwargs,
        dynamic_shapes=dynamic_shapes,
        preserve_module_call_signature=preserve_module_call_signature,
        strict=strict,
    )
