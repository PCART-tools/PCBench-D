def _export_to_aten_ir(
    mod: torch.nn.Module,
    fake_args,
    fake_kwargs,
    fake_params_buffers,
    constant_attrs: ConstantAttrMap,
    produce_guards_callback=None,
    *,
    transform=lambda x: x,  # TODO(zhxchen17) Revisit if this is needed later.
    pre_dispatch=False,
    decomp_table=None,
    _check_autograd_state: bool = True,
    _is_torch_jit_trace: bool = False,
    _prettify_placeholder_names: bool = True,
    decompose_custom_triton_ops: bool = False,
) -> ATenExportArtifact:
    # [NOTE] If the user is exporting under training mode, we want to detect if there is any
    # state change in the autograd global state and error. If the user is exporting under inference
    # mode, we don't care. At predispatch level, we don't care about the state change.
    is_grad_enabled = torch._C.is_grad_enabled()
    grad_safe_guard = nullcontext()
    # export_to_aten_ir is called when we decompose the ep into inference IR
    # In that setting, we actually shouldn't check the state change as at this point,
    # because the intention is specalizing to inference.
    if _check_autograd_state:
        if not pre_dispatch and is_grad_enabled:
            grad_safe_guard = AutogradStateOpsFailSafeguard()  # type: ignore[assignment]

    custom_triton_ops_decomposition_ctx = (
        nullcontext
        if decompose_custom_triton_ops
        else _disable_custom_triton_op_functional_decomposition
    )
    # This _reparametrize_module makes sure inputs and module.params/buffers have the same fake_mode,
    # otherwise aot_export_module will error out because it sees a mix of fake_modes.
    # And we want aot_export_module to use the fake_tensor mode in dynamo to keep the pipeline easy to reason about.
    with (
        torch.nn.utils.stateless._reparametrize_module(
            mod,
            fake_params_buffers,
            tie_weights=True,
            strict=True,
            stack_weights=True,
        ),
        grad_safe_guard,
        _ignore_backend_decomps(),
        _compiling_state_context(),
        custom_triton_ops_decomposition_ctx(),
    ):
        gm, graph_signature = transform(aot_export_module)(
            mod,
            fake_args,
            trace_joint=False,
            pre_dispatch=pre_dispatch,
            decompositions=decomp_table,
            kwargs=fake_kwargs,
        )

    def _maybe_fixup_gm_and_output_node_meta(old_gm, new_gm):
        if isinstance(old_gm, torch.fx.GraphModule):
            if hasattr(old_gm, "meta"):
                new_gm.meta.update(old_gm.meta)
            old_output_node = list(old_gm.graph.nodes)[-1]
            new_output_node = list(new_gm.graph.nodes)[-1]
            assert old_output_node.op == "output" and new_output_node.op == "output"
            # make sure we don't override any meta
            assert len(new_output_node.meta) == 0
            new_output_node.meta.update(old_output_node.meta)

    # TODO unfortunately preserving graph-level metadata and output node's meta
    # is not working well with aot_export. So we manually copy it.
    # (The node-level meta is addressed above.)
    _maybe_fixup_gm_and_output_node_meta(mod, gm)

    # Run produce guards before we handle runtime asserts.
    # This means we run the export solver before the runtime asserts pass.
    # Right now this doesn't mean much - the export solver is only there for suggested fixes,
    # and we won't even get to constraint solving if that's needed.
    # But if in future we want to control what runtime asserts are emitted for export,
    # or rely on produce_guards + solver for some simplification on runtime asserts, this probably makes sense.
    if produce_guards_callback:
        try:
            produce_guards_callback(gm)
        except (ConstraintViolationError, ValueRangeError) as e:
            raise UserError(UserErrorType.CONSTRAINT_VIOLATION, str(e))  # noqa: B904

    return _produce_aten_artifact(
        gm=gm,
        mod=mod,
        constant_attrs=constant_attrs,
        graph_signature=graph_signature,
        pre_dispatch=pre_dispatch,
        fake_args=fake_args,
        fake_kwargs=fake_kwargs,
        fake_params_buffers=fake_params_buffers,
        _prettify_placeholder_names=_prettify_placeholder_names,
    )
