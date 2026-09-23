def _strict_export(
    mod: torch.nn.Module,
    args: tuple[Any, ...],
    kwargs: dict[str, Any],
    dynamic_shapes: Optional[Union[dict[str, Any], tuple[Any], list[Any]]],
    preserve_module_call_signature: tuple[str, ...],
    pre_dispatch: bool,
    original_state_dict: dict[str, Any],
    orig_in_spec: TreeSpec,
    allow_complex_guards_as_runtime_asserts: bool,
    _is_torch_jit_trace: bool,
) -> ExportArtifact:
    lower_to_aten = functools.partial(_export_to_aten_ir, pre_dispatch=pre_dispatch)
    return _strict_export_lower_to_aten_ir(
        mod=mod,
        args=args,
        kwargs=kwargs,
        dynamic_shapes=dynamic_shapes,
        preserve_module_call_signature=preserve_module_call_signature,
        pre_dispatch=pre_dispatch,
        original_state_dict=original_state_dict,
        orig_in_spec=orig_in_spec,
        allow_complex_guards_as_runtime_asserts=allow_complex_guards_as_runtime_asserts,
        _is_torch_jit_trace=_is_torch_jit_trace,
        lower_to_aten_callback=lower_to_aten,
    )
