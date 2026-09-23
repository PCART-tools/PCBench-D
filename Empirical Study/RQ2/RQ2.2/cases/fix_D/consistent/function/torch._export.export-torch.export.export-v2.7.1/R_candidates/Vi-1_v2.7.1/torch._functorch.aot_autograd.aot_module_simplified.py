def aot_module_simplified(
    mod: nn.Module,
    args,
    fw_compiler: AOTDispatchCompiler,
    bw_compiler: Optional[AOTDispatchCompiler] = None,
    partition_fn: Callable = default_partition,
    decompositions: Optional[dict] = None,
    keep_inference_input_mutations=False,
    inference_compiler: Optional[AOTDispatchCompiler] = None,
    cudagraphs: Optional[BoxedBool] = None,
) -> nn.Module:
    """
    This is the simplified or low overhead version of aot_module. For frontends
    like TorchDynamo, the input functions/modules to AOT are static and have
    unpacked inputs/outputs. This gives us an opportunity to remove the
        (1) pytree overhead to parse inputs/outputs,
        (2) AOT Autograd cache,
        (3) Reading of params/buffers in every forward call

    :func:`aot_module_simplified` removes these overheads.
    """
    params = {
        **dict(mod.named_parameters(remove_duplicate=False)),
        **dict(mod.named_buffers(remove_duplicate=False)),
    }
    params_flat, params_spec = pytree.tree_flatten(params)
    params_flat = list(params_flat)
    params_len = len(params_flat)

    if cudagraphs is None:
        cudagraphs = BoxedBool(torch._inductor.config.triton.cudagraphs)

    if bw_compiler is None:
        bw_compiler = fw_compiler
    if inference_compiler is None:
        inference_compiler = fw_compiler

    full_args = []
    # First, the params
    full_args.extend(params_flat)

    if tracing_context := torch._guards.TracingContext.try_get():
        tracing_context.params_flat = params_flat
        (
            tracing_context.params_flat_unwrap_subclasses,
            tracing_context.params_unwrapped_to_flat_index,
        ) = unwrap_tensor_subclasses_with_indices_to_original(params_flat)

    # Next, the input args
    full_args.extend(args)

    (
        aot_autograd_arg_pos_to_source,
        static_input_indices,
    ) = _try_get_metadata_from_dynamo(mod, params.keys(), len(full_args))

    dynamic_shapes = False
    for x in full_args:
        if isinstance(x, FakeTensor):
            dynamic_shapes = x.fake_mode.shape_env is not None
            break

    aot_config = AOTConfig(
        fw_compiler=fw_compiler,
        bw_compiler=bw_compiler,
        inference_compiler=inference_compiler,
        partition_fn=partition_fn,
        decompositions=decompositions,
        num_params_buffers=params_len,
        aot_id=next(AOT_COUNTER),
        keep_inference_input_mutations=keep_inference_input_mutations,
        dynamic_shapes=dynamic_shapes,
        aot_autograd_arg_pos_to_source=aot_autograd_arg_pos_to_source,
        static_input_indices=static_input_indices,
        is_export=False,
        no_tangents=False,
        cache_info=None,
    )
    fake_mode, shape_env = construct_fake_mode(full_args, aot_config)
    fake_flat_args = process_inputs(full_args, aot_config, fake_mode, shape_env)

    def dispatch_and_compile():
        functional_call = create_functional_call(mod, params_spec, params_len)
        with compiled_autograd._disable():
            compiled_fn, _ = create_aot_dispatcher_function(
                functional_call,
                fake_flat_args,
                aot_config,
                fake_mode,
                shape_env,
            )
        return compiled_fn

    # We only care if the forward will return an OutputCode.
    if isinstance(fw_compiler, SerializableAOTDispatchCompiler):
        local = should_use_local_autograd_cache()
        remote = should_use_remote_autograd_cache()
        if local or remote:
            set_feature_use("aot_autograd_remote_cache", remote)
            compiled_fn = AOTAutogradCache.load(
                dispatch_and_compile,
                mod,
                fake_flat_args,
                aot_config,
                cudagraphs,
                local,
                remote,
            )
        else:
            compiled_fn = dispatch_and_compile()
    else:
        compiled_fn = dispatch_and_compile()

    if isinstance(mod, torch._dynamo.utils.GmWrapper):
        # This function is called by the flatten_graph_inputs wrapper, which boxes
        # the inputs so that they can be freed before the end of this scope.
        # For overhead reasons, this is not the default wrapper, see comment:
        # https://github.com/pytorch/pytorch/pull/122535/files#r1560096481
        def boxed_forward(runtime_args: list[Any]):
            flat_args = []
            flat_args.extend(params_flat)
            flat_args.extend(runtime_args)
            runtime_args.clear()
            return compiled_fn(flat_args)

        # Just for convenience
        boxed_forward.zero_grad = mod.zero_grad
        boxed_forward.named_parameters = mod.named_parameters
        boxed_forward.named_buffers = mod.named_buffers
        return boxed_forward

    # TODO: There is something deeply wrong here; compiled_fn running with
    # the boxed calling convention, but aot_module_simplified somehow
    # historically returned a function that was not the boxed calling
    # convention.  This should get fixed...
    # NB: GraphModule/nn.Module rely on the non-boxed calling convention here
    def forward(*runtime_args: tuple[Any]):
        full_args = []
        full_args.extend(params_flat)
        full_args.extend(runtime_args)
        return compiled_fn(full_args)

    # Just for convenience
    forward.zero_grad = mod.zero_grad
    forward.named_parameters = mod.named_parameters
    forward.named_buffers = mod.named_buffers

    return forward
