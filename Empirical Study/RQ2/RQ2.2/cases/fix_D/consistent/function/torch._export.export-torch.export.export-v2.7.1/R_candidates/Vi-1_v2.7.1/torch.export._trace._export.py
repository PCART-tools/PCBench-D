@_log_export_wrapper
@_disable_prexisiting_fake_mode
def _export(
    mod: torch.nn.Module,
    args: tuple[Any, ...],
    kwargs: Optional[dict[str, Any]] = None,
    dynamic_shapes: Optional[Union[dict[str, Any], tuple[Any], list[Any]]] = None,
    *,
    strict: bool = True,
    preserve_module_call_signature: tuple[str, ...] = (),
    pre_dispatch: bool = False,
    allow_complex_guards_as_runtime_asserts: bool = False,
    _is_torch_jit_trace: bool = False,
) -> ExportedProgram:
    """
    Traces either an nn.Module's forward function or just a callable with PyTorch
    operations inside and produce a ExportedProgram.

    Args:
        f: the `nn.Module` to trace.

        args: example positional inputs.

        kwargs: optional example keyword inputs.

        dynamic_shapes:
         An optional argument where the type should either be:
         1) a dict from argument names of ``f`` to their dynamic shape specifications,
         2) a tuple that specifies dynamic shape specifications for each input in original order.
         If you are specifying dynamism on keyword args, you will need to pass them in the order that
         is defined in the original function signature.

         The dynamic shape of a tensor argument can be specified as either
         (1) a dict from dynamic dimension indices to :func:`Dim` types, where it is
         not required to include static dimension indices in this dict, but when they are,
         they should be mapped to None; or (2) a tuple / list of :func:`Dim` types or None,
         where the :func:`Dim` types correspond to dynamic dimensions, and static dimensions
         are denoted by None. Arguments that are dicts or tuples / lists of tensors are
         recursively specified by using mappings or sequences of contained specifications.

        preserve_module_call_signature: A list of submodule paths for which the original
            calling conventions are preserved as metadata.

        allow_complex_guards_as_runtime_asserts:
         With the current dynamic shapes language for dims and derived dims, we can run into constraints
         that are not expressible with the language. For example, flattening a matrix and adding to a vector,
         both fully dynamic (i.e. x.reshape([-1]) + y) emits a guard s0 * s1 = s2, which is not expressible.
         By default, we either raise a constraint violation error or specialize to static values.
         If this flag is set to True, we avoid erroring out and instead allow complex constraints to exist as runtime
         assertions in the graph. The sympy interpreter (torch/utils/_sympy/interp.py) will produce the math ops
         required to compute and assert the value of the guard (e.g. sym_size_int, eq, _assert_scalar).
         Additionally, if TORCH_DYNAMO_DO_NOT_EMIT_RUNTIME_ASSERTS=1 is specified, we will allow complex constraints
         while not emitting runtime asserts, returning a cleaner graph with lesser guarantees around dynamic shapes.

    Returns:
        An ExportedProgram containing the traced method.
    """

    from torch._utils_internal import export_training_ir_rollout_check

    global _EXPORT_FLAGS, _EXPORT_MODULE_HIERARCHY
    _EXPORT_MODULE_HIERARCHY = _get_module_hierarchy(mod)

    flags = set()
    flags.add("strict" if strict else "non_strict")
    flags.add("pre_dispatch" if pre_dispatch else "aot_dispatch")
    _EXPORT_FLAGS = flags

    log_export_usage(event="export.enter", flags=_EXPORT_FLAGS)

    dtrace_structured("export", payload_fn=lambda: "start!")

    # NOTE Export training IR rollout
    # Old export calls export._trace(pre_dispatch=True)
    # and there are still lot of internal/OSS callsites that
    # use export._trace(pre_dispatch=True) directly. Therefore,
    # it makes more sense to do the switch here.
    # export_training_ir_rollout_check returns True in OSS
    # while internally it returns False UNLESS otherwise specified.
    if pre_dispatch and export_training_ir_rollout_check():
        ep = _export_for_training(
            mod,
            args,
            kwargs,
            dynamic_shapes,
            strict=strict,
            preserve_module_call_signature=preserve_module_call_signature,
        )
        dtrace_structured("exported_program", payload_fn=lambda: str(ep))
        return ep

    (
        args,
        kwargs,
        original_in_spec,
        dynamic_shapes,
    ) = _process_export_inputs(mod, args, kwargs, dynamic_shapes)

    original_state_dict = _get_original_state_dict(mod)

    # Call the appropriate export function based on the strictness of tracing.
    export_func = _strict_export if strict else _non_strict_export

    export_artifact = export_func(  # type: ignore[operator]
        mod,
        args,
        kwargs,
        dynamic_shapes,
        preserve_module_call_signature,
        pre_dispatch,
        original_state_dict,
        original_in_spec,
        allow_complex_guards_as_runtime_asserts,
        _is_torch_jit_trace,
    )
    export_graph_signature: ExportGraphSignature = export_artifact.aten.sig

    forward_arg_names = (
        _get_forward_arg_names(mod, args, kwargs) if not _is_torch_jit_trace else None
    )
    inline_constraints = _get_inline_constraints(export_artifact.fake_mode)
    # The unbacked symint symbols are updated in aot_export
    # so we serialize them here instead of inside dynamo.
    # Note: this step must be before _get_range_constraints.
    export_artifact.aten.gm.meta["inline_constraints"] = inline_constraints
    range_constraints = _get_range_constraints(
        export_artifact,
        _combine_args(mod, args, kwargs, _is_torch_jit_trace=_is_torch_jit_trace),
        dynamic_shapes,
    )
    gm, module_call_graph = _get_module_call_graph(
        export_artifact,
        preserve_module_call_signature,
        strict,
        forward_arg_names,
    )

    _verify_nn_module_stack(gm)
    _verify_stack_trace(gm)
    if not _is_torch_jit_trace:
        _verify_placeholder_names(gm, export_graph_signature)

    # Remove Proxy because they cannot be deepcopied or pickled.
    torch._export.utils.remove_proxy_from_state_dict(original_state_dict, in_place=True)

    from torch._export.verifier import Verifier

    _update_gm_meta_if_possible(gm, mod)

    exported_program = ExportedProgram(
        root=gm,
        graph=gm.graph,
        graph_signature=export_graph_signature,
        state_dict=original_state_dict,
        range_constraints=range_constraints,
        module_call_graph=module_call_graph,
        example_inputs=(args, kwargs),
        constants=export_artifact.aten.constants,
        verifiers=[Verifier],
    )

    dtrace_structured("exported_program", payload_fn=lambda: str(exported_program))

    return exported_program
