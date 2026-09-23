def aot_dispatch_base(
    flat_fn,
    flat_args: list[Any],
    aot_config: AOTConfig,
    *,
    fw_metadata: ViewAndMutationMeta,
) -> DispatchReturn:
    """
    Handles functions that don't need autograd. Runs wrappers and compiles with fw_compiler.
    """
    wrappers = _create_wrappers_for_dispatch(needs_autograd=False)
    flat_fn, flat_args, fw_metadata = pre_compile(
        wrappers, flat_fn, flat_args, aot_config, fw_metadata=fw_metadata
    )
    fw_module, updated_flat_args, maybe_subclass_meta = aot_dispatch_base_graph(  # type: ignore[misc]
        flat_fn, flat_args, aot_config, fw_metadata=fw_metadata
    )
    # Save the forward_graph_str right after aot_dispatch_base_graph,
    # to save in the cache
    aot_forward_graph_str = None
    if aot_config.cache_info is not None:
        aot_forward_graph_str = fw_module.print_readable(
            print_output=False,
            include_stride=True,
            include_device=True,
            fast_sympy_print=True,
        )

    fakified_out_wrapper = FakifiedOutWrapper()
    (
        fw_module,
        updated_flat_args,
        fw_metadata,
    ) = fakified_out_wrapper.pre_compile(
        fw_module, updated_flat_args, aot_config, fw_metadata=fw_metadata
    )
    functionalized_rng_wrapper = FunctionalizedRngRuntimeWrapper()
    (
        fw_module,
        updated_flat_args,
        fw_metadata,
    ) = functionalized_rng_wrapper.pre_compile(
        fw_module, updated_flat_args, aot_config, fw_metadata=fw_metadata
    )
    assert isinstance(fw_module, GraphModule)

    if aot_config.enable_log:
        trace_structured(
            "artifact",
            metadata_fn=lambda: {
                "name": "torch._functorch.config",
                "encoding": "string",
            },
            payload_fn=lambda: torch._functorch.config.get_config_copy(),
        )

    disable_amp = torch._C._is_any_autocast_enabled()
    context = torch._C._DisableAutocast if disable_amp else nullcontext

    with context(), track_graph_compiling(aot_config, "inference"):
        compiler = (
            aot_config.inference_compiler
            if aot_config.inference_compiler is not None
            else aot_config.fw_compiler
        )

        if tracing_context := torch._guards.TracingContext.try_get():
            tracing_context.fw_metadata = (
                fw_metadata
                if maybe_subclass_meta is None
                else maybe_subclass_meta.fw_metadata
            )

        with TracingContext.report_output_strides() as fwd_output_strides:
            fake_mode = detect_fake_mode()
            if fake_mode is not None and fake_mode.shape_env is not None:
                tensorify_python_scalars(fw_module, fake_mode.shape_env, fake_mode)
            compiled_fw = compiler(fw_module, updated_flat_args)

        if fakified_out_wrapper.needs_post_compile:
            fakified_out_wrapper.set_fwd_output_strides(fwd_output_strides)

    make_runtime_safe(fw_metadata, maybe_subclass_meta)

    # However, RuntimeWrapper does not expect the rng offsets in the
    # output. So, we have to create another wrapper and take out the offset. As
    # a result, we have to account for not boxed_call compilers as well.
    if not getattr(compiled_fw, "_boxed_call", False):
        compiled_fw = make_boxed_func(compiled_fw)

    # Create a wrapper to set up the rng functionalize and fakified out bits
    compiled_fw = functionalized_rng_wrapper.post_compile(
        compiled_fw, aot_config, runtime_metadata=fw_metadata
    )
    cache_info = aot_config.cache_info
    if cache_info is not None:
        if hasattr(compiled_fw, "_fx_graph_cache_key"):
            time_taken_ns = time.time_ns() - cache_info.start_time_ns
            guards_expr = AOTAutogradCache.generate_guards_expression(cache_info)
            entry = AOTAutogradCache.make_entry(
                compiled_fw_func=compiled_fw,  # type: ignore[arg-type]
                compiled_bw_func=None,
                aot_joint_graph_str=None,
                aot_forward_graph_str=aot_forward_graph_str,
                aot_backward_graph_str=None,
                runtime_metadata=fw_metadata,
                dispatch_wrappers=wrappers,
                maybe_subclass_meta=maybe_subclass_meta,
                num_fw_outs_saved_for_bw=None,
                indices_of_inps_to_detach=[],
                forward_time_taken_ns=time_taken_ns,
                backward_time_taken_ns=0,
                sanitized_aot_config=sanitize_aot_config(aot_config),
                guards_expr=guards_expr,
                backward_state_indices=None,
                num_symints_saved_for_bw=None,
                serialized_bw_module=None,
            )
            AOTAutogradCache.save(
                cache_info.cache_key, entry, remote=should_use_remote_autograd_cache()
            )

    compiled_fw = fakified_out_wrapper.post_compile(
        compiled_fw,
        aot_config,
        runtime_metadata=fw_metadata,
    )

    compiled_fw = EffectTokensWrapper().post_compile(
        compiled_fw,
        aot_config,
        runtime_metadata=fw_metadata,
    )

    # Why do we need to pass in num_fw_outs_saved_for_bw?
    # See Note: [Partitioner handling for Subclasses, Part 2]
    compiled_fw = AOTDispatchSubclassWrapper(
        trace_joint=False,
        # TODO: once we use pre_compile this will be flat_fn at the top of this function
        fw_only=None,
        maybe_subclass_meta=maybe_subclass_meta,
        num_fw_outs_saved_for_bw=None,
    ).post_compile(
        compiled_fw,
        aot_config,  # not used
        runtime_metadata=fw_metadata,
    )

    if not getattr(compiled_fw, "_boxed_call", False):
        compiled_fw = make_boxed_func(compiled_fw)

    compiled_fn = RuntimeWrapper(
        indices_of_inps_to_detach=[],
        trace_joint=False,
        disable_amp=disable_amp,
    ).post_compile(
        compiled_fw,
        aot_config,
        runtime_metadata=fw_metadata,
    )

    compiled_fn = post_compile(
        wrappers, compiled_fn, aot_config, runtime_metadata=fw_metadata
    )
    return compiled_fn
