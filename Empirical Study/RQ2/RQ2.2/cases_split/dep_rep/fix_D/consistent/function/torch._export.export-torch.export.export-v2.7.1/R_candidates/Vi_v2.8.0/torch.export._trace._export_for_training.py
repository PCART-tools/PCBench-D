@_log_export_wrapper
@_disable_prexisiting_fake_mode
def _export_for_training(
    mod: torch.nn.Module,
    args: tuple[Any, ...],
    kwargs: Optional[dict[str, Any]] = None,
    dynamic_shapes: Optional[Union[dict[str, Any], tuple[Any], list[Any]]] = None,
    *,
    strict: bool = True,
    preserve_module_call_signature: tuple[str, ...] = (),
) -> ExportedProgram:
    global _EXPORT_MODULE_HIERARCHY
    _EXPORT_MODULE_HIERARCHY = _get_module_hierarchy(mod)

    (
        args,
        kwargs,
        orig_in_spec,
        dynamic_shapes,
        verify_additional_inputs,
    ) = _process_export_inputs(mod, args, kwargs, dynamic_shapes)

    original_state_dict = _get_original_state_dict(mod)

    # Call the appropriate export function based on the strictness of tracing.
    export_func = _strict_export if strict else _non_strict_export

    export_artifact = export_func(
        mod=mod,
        args=args,
        kwargs=kwargs,
        dynamic_shapes=dynamic_shapes,
        preserve_module_call_signature=preserve_module_call_signature,
        orig_in_spec=orig_in_spec,
        allow_complex_guards_as_runtime_asserts=False,
        _is_torch_jit_trace=False,
        _to_aten_func=_export_to_aten_ir_make_fx,
    )

    export_graph_signature = export_artifact.aten.sig

    forward_arg_names = _get_forward_arg_names(mod, args, kwargs)
    inline_constraints = _get_inline_constraints(export_artifact.fake_mode)
    # The unbacked symint symbols are updated in aot_export
    # so we serialize them here instead of inside dynamo.
    # Note: _get_range_constraints depends on "inline_constraints" to be set.
    export_artifact.aten.gm.meta["inline_constraints"] = inline_constraints
    range_constraints = _get_range_constraints(
        mod,
        export_artifact,
        args,
        kwargs,
        dynamic_shapes,
    )
    # The returned the gm is in-place modified
    gm, module_call_graph = _get_module_call_graph(
        export_artifact,
        preserve_module_call_signature,
        strict,
        forward_arg_names,
    )

    _verify_nn_module_stack(gm)
    _verify_stack_trace(gm)
    _verify_placeholder_names(gm, export_graph_signature)

    _update_gm_meta_if_possible(gm, mod)

    from torch._export.verifier import TrainingIRVerifier

    exported_program = ExportedProgram(
        root=gm,
        graph=gm.graph,
        graph_signature=export_graph_signature,
        state_dict=original_state_dict,
        range_constraints=range_constraints,
        module_call_graph=module_call_graph,
        example_inputs=(args, kwargs),
        constants=export_artifact.aten.constants,
        verifiers=[TrainingIRVerifier],
    )

    verify_additional_inputs(exported_program)
    return exported_program
