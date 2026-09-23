def aot_dispatch_autograd_graph(
    flat_fn,
    flat_args: list[Any],
    aot_config: AOTConfig,
    *,
    fw_metadata: ViewAndMutationMeta,
) -> tuple[torch.fx.GraphModule, tuple[list[Any], list[Any]], Optional[SubclassMeta]]:
    # traced_tangents corresponds to the set of outputs in the traced forward that should get grad_outputs in the traced backward.
    # It includes outputs of the original forward, *and* any updated inputs due to input mutations.
    # However, it does *not* include any outputs that are aliases of inputs or intermediates, or any metadata-only input mutations.
    joint_inputs = (flat_args, fw_metadata.traced_tangents)

    fn_prepared_for_autograd = fn_prepped_for_autograd(
        flat_fn,
        fw_metadata,
    )
    joint_fn_to_trace = create_joint(fn_prepared_for_autograd, aot_config=aot_config)

    joint_fn_to_trace, updated_joint_inputs = create_functionalized_fn(
        joint_fn_to_trace,
        joint_inputs,
        meta=fw_metadata,
        aot_config=aot_config,
        trace_joint=True,
    )

    # TODO: replace with AOTDispatchSubclassWrapper once we refactor
    # fn_input_mutations_to_outputs and create_functionalized_fn
    # into CompilerWrappers.
    subclass_tracing_info = aot_dispatch_subclass(
        joint_fn_to_trace,
        updated_joint_inputs,
        is_joint_structure=True,
        meta=fw_metadata,
        fw_only=flat_fn,
    )

    joint_fn_to_trace = subclass_tracing_info.plain_tensor_trace_fn
    updated_joint_inputs = subclass_tracing_info.plain_tensor_args

    (joint_fn_to_trace, updated_joint_inputs) = handle_effect_tokens_fn(
        joint_fn_to_trace,
        updated_joint_inputs,
        meta=fw_metadata,
        trace_joint=True,
    )

    # When we call _create_graph, this may mutate the metadata of joint
    # inputs.  But callers are expecting to get the original joint inputs.  So
    # we make aliases of all the inputs to make sure we have a copy that
    # doesn't get modified.
    #
    # This destroys requires_grad/grad_fn information.  However, backends
    # beneath AOTAutograd are indifferent to this information, so it doesn't
    # matter.

    fake_mode = detect_fake_mode()
    if fake_mode:
        saved_updated_joint_inputs = pytree.tree_map_only(
            torch.Tensor, _detach_and_copy_item_memo, updated_joint_inputs
        )
    else:
        saved_updated_joint_inputs = pytree.tree_map_only(
            torch.Tensor, lambda t: t.detach(), updated_joint_inputs
        )
    maybe_subclass_meta = subclass_tracing_info.maybe_subclass_meta

    fx_g = _create_graph(joint_fn_to_trace, updated_joint_inputs, aot_config=aot_config)

    # There should be *NO* mutating ops in the graph at this point.
    assert_functional_graph(fx_g.graph)

    # Redundant with the check above, but worth having in case tracing introduced
    # a fake tensor. Unlikely.
    # See Note: [Fake Modules and AOTAutograd]
    torch._dynamo.utils.assert_no_fake_params_or_buffers(fx_g)
    fx_g.graph.eliminate_dead_code()
    copy_fwd_metadata_to_bw_nodes(fx_g)
    fx_g.recompile()

    # TODO: in AOTAutograd, we create metadata like _indices_of_inps_to_detach to detect
    # when we need to manually detach() some inputs in the forward.
    # Higher order ops might eventually need to do the same.
    if aot_config.is_export:
        assert (
            maybe_subclass_meta is None
        ), "aot_export_module does not support tensor subclass inputs for now."
    return fx_g, saved_updated_joint_inputs, maybe_subclass_meta
