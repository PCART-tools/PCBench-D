def compile_fx(
    model_: GraphModule,
    example_inputs_: Sequence[InputType],
    inner_compile: Callable[..., OutputCode] = compile_fx_inner,
    config_patches: Optional[dict[str, Any]] = None,
    decompositions: Optional[dict[OpOverload, Callable[..., Any]]] = None,
    ignore_shape_env: bool = False,
) -> Union[Callable[[list[object]], Sequence[torch.Tensor]], str, list[str], Weights]:
    """
    Main entry point for compiling given FX graph.  Despite the fact that this
    lives in :mod:`torch._inductor`, this function is responsible for calling
    into AOT Autograd (and we will eventually get a callback to
    ``inner_compile`` to perform actual compilation.  In other words, this
    function orchestrates end-to-end compilation for the inductor backend when
    you use :func:`torch.compile`.

    NB: This function TAKES OWNERSHIP of the input ``model_`` and can potentially
    mutate it!  Make a copy if you need to preserve the original GraphModule.
    """

    # Some arguments trigger a recursive call to compile_fx.  Handle these
    # short circuits first, before anything else

    if config_patches:
        with config.patch(config_patches):
            return compile_fx(
                model_,
                example_inputs_,
                # need extra layer of patching as backwards is compiled out of scope
                inner_compile=config.patch(config_patches)(inner_compile),
                decompositions=decompositions,
                ignore_shape_env=ignore_shape_env,
            )

    # TODO: This probably shouldn't be a recursive call
    if config.cpp_wrapper:
        with (
            config.patch(
                {
                    "cpp_wrapper": False,  # reset to break recursive call to compile_fx
                    **get_cpp_wrapper_config(),
                }
            ),
            V.set_real_inputs(example_inputs_),
        ):
            inputs_: Sequence[InputType] = example_inputs_

            if isinstance(model_, GraphModule):
                fake_inputs = [
                    node.meta.get("val")
                    for node in model_.graph.nodes
                    if node.op == "placeholder"
                ]
                # Replace non-tensor (constant) inputs with Nones, since these are not being
                # used anyways by the graph
                fake_inputs = [
                    inp if isinstance(inp, torch.Tensor) else None
                    for inp in fake_inputs
                ]

                if any(v is not None for v in fake_inputs):
                    # Validate devices before switching to fake tensors.
                    for idx, fi, i in zip(count(), fake_inputs, inputs_):
                        if fi is not None:
                            assert isinstance(i, torch.Tensor)
                            if fi.device != i.device:
                                raise ValueError(
                                    f"Device mismatch between fake input and example input at position #{idx}: "
                                    f"{fi.device} vs {i.device}. If the model was exported via torch.export(), "
                                    "make sure torch.export() and torch.aot_compile() run on the same device."
                                )
                    inputs_ = fake_inputs  # type: ignore[assignment]
            from torch._export.non_strict_utils import _fakify_script_objects

            fake_mode = detect_fake_mode(inputs_)
            with _fakify_script_objects(model_, inputs_, {}, fake_mode) as (
                patched_mod,
                fake_args,
                _,
                _,
                _,
            ):
                return compile_fx(
                    patched_mod,
                    fake_args,
                    inner_compile=functools.partial(inner_compile, cpp_wrapper=True),
                    decompositions=decompositions,
                    ignore_shape_env=ignore_shape_env,
                )

    recursive_compile_fx = functools.partial(
        compile_fx,
        inner_compile=inner_compile,
        decompositions=decompositions,
        ignore_shape_env=ignore_shape_env,
    )

    if not graph_returns_tuple(model_):
        return make_graph_return_tuple(
            model_,
            example_inputs_,
            recursive_compile_fx,
        )

    if isinstance(model_, GraphModule) and isinstance(
        model_.graph._codegen, _PyTreeCodeGen
    ):
        # this graph is the result of dynamo.export()
        return handle_dynamo_export_graph(
            model_,
            example_inputs_,
            recursive_compile_fx,
        )

    # Do the actual work

    with (
        _use_lazy_graph_module(dynamo_config.use_lazy_graph_module),
        enable_python_dispatcher(),
        torch.fx.traceback.preserve_node_meta(config.trace.enabled),
    ):
        # Pre-grad passes cannot be run if we weren't given a GraphModule.
        # Dynamo will always produce a GraphModule, but this handles cases
        # where a user directly passes a plain Module with the intention of
        # having AOTAutograd trace it.
        # TODO: Get rid of this?
        if isinstance(model_, GraphModule):
            # "before_pre_grad_graph" is used in inductor provenance
            # tracking highlighter front-end.
            trace_structured(
                "artifact",
                metadata_fn=lambda: {
                    "name": "before_pre_grad_graph",
                    "encoding": "string",
                },
                payload_fn=lambda: model_.print_readable(
                    print_output=False, include_stride=True, include_device=True
                )
                + f"\n\n # graph id: {id(model_.graph)}",
            )
            pre_grad_graphs_log.debug(
                "%s",
                lazy_format_graph_code(
                    "BEFORE PRE GRAD",
                    model_,
                    include_stride=True,
                    include_device=True,
                    colored=True,
                ),
            )
            torch._inductor.debug._pre_grad_graph_id = id(model_.graph)

            model_ = _recursive_pre_grad_passes(model_, example_inputs_)
            trace_structured(
                "artifact",
                metadata_fn=lambda: {
                    "name": "after_pre_grad_graph",
                    "encoding": "string",
                },
                payload_fn=lambda: model_.print_readable(
                    print_output=False, include_stride=True, include_device=True
                )
                + f"\n\n # graph id: {id(model_.graph)}",
            )

        # TODO: Move this before recursive pre-grad passes
        # NB: This short circuit never occurs for Dynamo produced graphs
        # (which are pre-flattened)
        if any(isinstance(x, (list, tuple, dict)) for x in example_inputs_):
            return flatten_graph_inputs(
                model_,
                example_inputs_,
                recursive_compile_fx,
            )

        assert not config._raise_error_for_testing

        num_example_inputs = len(example_inputs_)

        # Although cudagraphs may have been enabled via config, various
        # conditions (which are tested within the bowels of Inductor) may
        # force cudagraphs to be disabled.  This mutable box lets us retrieve
        # the final determination if cudagraphs actually can be used or not.
        cudagraphs = BoxedBool(config.triton.cudagraphs)

        # See [Backward Generation Handling]
        forward_device = BoxedDeviceIndex(None)

        # TODO: The modern style is to use CompileId from TracingContext to
        # identify Inductor compilation.  However, this CompileId cannot
        # uniquely identify multiple Inductor compilations that arise from
        # DDPOptimizer
        graph_id = next(_graph_counter)

        decompositions = (
            decompositions if decompositions is not None else select_decomp_table()
        )

        def fw_compiler_base(
            gm: GraphModule,
            example_inputs: Sequence[InputType],
            is_inference: bool,
        ) -> OutputCode:
            with dynamo_utils.dynamo_timed("compile_fx.<locals>.fw_compiler_base"):
                if is_inference:
                    # partition_fn won't be called
                    _recursive_joint_graph_passes(gm)

                fixed = torch._inductor.utils.num_fw_fixed_arguments(
                    num_example_inputs, len(example_inputs)
                )

                model_outputs_node = output_node(gm)
                if config.keep_output_stride:
                    model_outputs = pytree.arg_tree_leaves(*model_outputs_node.args)
                    num_model_outputs = len(model_outputs)

                    context = torch._guards.TracingContext.try_get()
                    # See Note [User Outputs in the inductor graph]
                    if context is not None and context.fw_metadata and not is_inference:
                        original_output_start_index = (
                            context.fw_metadata.num_mutated_inp_runtime_indices
                        )
                    else:
                        original_output_start_index = 0

                    if isinstance(model_, GraphModule):
                        *_, orig_model_outputs_node = model_.graph.nodes
                        assert orig_model_outputs_node.op == "output"
                        orig_model_outputs, _ = pytree.tree_flatten(
                            orig_model_outputs_node.args
                        )
                        num_orig_model_outputs = len(orig_model_outputs)
                    else:
                        num_orig_model_outputs = num_model_outputs

                    assert num_orig_model_outputs <= num_model_outputs

                    # Note [User Outputs in the inductor graph]
                    # We makes the following assumption
                    # For inference
                    #   len(orig_model_outputs) == len(model_outputs)
                    # For training
                    #   len(orig_model_outputs) <= len(model_outputs)
                    # During training, most of the time the model_outputs starts with
                    # original module's outputs followed by saved activations.
                    # But this can be not true if the model have inplace updated tensors.
                    # AOTAutograd will make those tensors being returned before the original
                    # module's output.
                    # To make things safe, we'll use original_output_start_index field
                    # set by AOTAutograd to decide where the original module outputs start.
                    orig_output_end_idx = (
                        original_output_start_index + num_orig_model_outputs
                    )
                    # Sanity check: we are about to splice out the "user" outputs from the full set
                    # of "graph" outputs. Make sure we're within bounds.
                    assert orig_output_end_idx <= num_model_outputs

                    model_outputs_node.meta["user_visible_output_idxs"] = [
                        idx
                        for idx in range(
                            original_output_start_index, orig_output_end_idx
                        )
                        if isinstance(model_outputs[idx], torch.fx.Node)
                    ]
                else:
                    model_outputs_node.meta["user_visible_output_idxs"] = []

                # We also mark the invoke_subgraph outputs as user_visible to
                # force the outputs of invoke_subgraph subgraph to follow the
                # original strides
                _recursive_record_user_visible_output_idxs(gm)

                return inner_compile(
                    gm,
                    example_inputs,
                    static_input_idxs=get_static_input_idxs(fixed),
                    cudagraphs=cudagraphs,
                    graph_id=graph_id,
                    is_inference=is_inference,
                    boxed_forward_device_index=forward_device,
                )

        fw_compiler: Callable[[GraphModule, Sequence[InputType]], OutputCode] = (
            functools.partial(fw_compiler_base, is_inference=False)
        )
        fw_compiler = SerializableAOTDispatchCompiler(OutputCode, fw_compiler)

        if config.freezing and not torch.is_grad_enabled():
            inference_compiler: Callable[..., Any] = functools.partial(
                fw_compiler_freezing,
                dynamo_model=model_,
                num_example_inputs=num_example_inputs,
                inner_compile=inner_compile,
                cudagraphs=cudagraphs,
                graph_id=graph_id,
                forward_device=forward_device,
            )
        else:
            inference_compiler = functools.partial(fw_compiler_base, is_inference=True)
            inference_compiler = SerializableAOTDispatchCompiler(
                OutputCode, inference_compiler
            )

        def partition_fn(
            gm: GraphModule,
            joint_inputs: Sequence[object],
            **kwargs: object,
        ) -> tuple[GraphModule, GraphModule]:
            cuda_context = get_cuda_device_context(gm)
            with cuda_context:
                # We can skip the invoke_subgraph because the
                # entire_partition_fn is called recursively for invoke_subgraph
                # in partitioning.
                _recursive_joint_graph_passes(gm, skip_invoke_subgraph=True)

            static_lifetime_input_indices: Optional[list[int]] = kwargs.pop(  # type: ignore[assignment]
                "static_lifetime_input_indices", None
            )

            with dynamo_utils.dynamo_timed(
                "min_cut_rematerialization_partition", log_pt2_compile_event=True
            ):
                return min_cut_rematerialization_partition(
                    gm,
                    joint_inputs,
                    compiler="inductor",
                    static_lifetime_input_indices=static_lifetime_input_indices,
                    **kwargs,
                )

        @compile_time_strobelight_meta(phase_name="backward")
        def bw_compiler(
            gm: GraphModule, example_inputs: Sequence[InputType]
        ) -> OutputCode:
            from torch._dynamo.convert_frame import compile_lock

            with (
                dynamo_utils.dynamo_timed("compile_fx.<locals>.bw_compiler"),
                compile_lock,
            ):
                model_outputs_node = output_node(gm)
                if config.bw_outputs_user_visible:
                    model_outputs = pytree.arg_tree_leaves(*model_outputs_node.args)
                    model_outputs_node.meta["user_visible_output_idxs"] = [
                        idx
                        for idx, n in enumerate(model_outputs)
                        if isinstance(n, torch.fx.Node)
                    ]
                else:
                    model_outputs_node.meta["user_visible_output_idxs"] = []

                fixed = count_tangents(gm)
                with (
                    config.patch(get_cpp_wrapper_config())
                    if config.cpp_wrapper
                    else contextlib.nullcontext()
                ):
                    return inner_compile(
                        gm,
                        example_inputs,
                        static_input_idxs=list(range(fixed)),
                        cudagraphs=cudagraphs,
                        is_backward=True,
                        graph_id=graph_id,
                        boxed_forward_device_index=forward_device,
                    )

        bw_compiler = SerializableAOTDispatchCompiler(OutputCode, bw_compiler)

        fake_mode = detect_fake_mode(
            example_inputs_
        ) or torch._subclasses.FakeTensorMode(allow_non_fake_inputs=True)
        tracing_context = (
            torch._guards.TracingContext.try_get()
            or torch._guards.TracingContext(fake_mode)
        )

        if V.aot_compilation:
            with functorch_config.patch(unlift_effect_tokens=True):
                gm, graph_signature = aot_export_module(
                    model_,
                    example_inputs_,
                    trace_joint=False,
                    decompositions=decompositions,
                )

                from torch._export.utils import _detect_fake_mode_from_gm

                fake_mode = _detect_fake_mode_from_gm(gm)
                # aot_export_module doesn't account for constant tensor attributes
                # so we end up having tensors that don't have fake vals attached.
                # This can happen when upstream export is non-strict where we
                # preserve the original module params/buffers. Once AOTI switches
                # to ep.run_decompositions() flow to lower to post-autograd opset
                # this will go away.
                for node in gm.graph.nodes:
                    if node.op == "get_attr" and "val" not in node.meta:
                        target = attrgetter(node.target)(gm)
                        if isinstance(target, torch.Tensor):
                            node.meta["val"] = fake_mode.from_tensor(
                                target, static_shapes=True
                            )
                        elif isinstance(target, torch.ScriptObject):
                            node.meta["val"] = (
                                torch._library.fake_class_registry.maybe_to_fake_obj(
                                    fake_mode, target
                                )
                            )
                        elif isinstance(target, FakeScriptObject):
                            node.meta["val"] = target

            unlifted_gm = _unlift_graph(model_, gm, graph_signature)
            if "dynamo_flat_name_to_original_fqn" in model_.meta:
                unlifted_gm.meta["dynamo_flat_name_to_original_fqn"] = model_.meta[
                    "dynamo_flat_name_to_original_fqn"
                ]

            if "dynamo_compile_id" in model_.meta:
                unlifted_gm.meta["dynamo_compile_id"] = model_.meta["dynamo_compile_id"]

            # Disable amp as in aot_dispatch_autograd (https://github.com/pytorch/pytorch/pull/86515)
            # In inference_compiler (fw_compiler_base), _recursive_joint_graph_passes will call into
            # _sfdp_init() to register patterns.
            # When fallback_random is set to True, the sdpa patterns will be traced during runtime.
            # If amp is turned on, the traced FP32 patterns will have prims.convert_element_type which
            # will be the same as the generated FP16 patterns.
            disable_amp = torch._C._is_any_autocast_enabled()
            context = (
                torch._C._DisableAutocast if disable_amp else contextlib.nullcontext
            )
            with V.set_fake_mode(fake_mode), compiled_autograd._disable(), context():
                return inference_compiler(unlifted_gm, example_inputs_)

        with (
            V.set_fake_mode(fake_mode),
            torch._guards.tracing(tracing_context),
            compiled_autograd._disable(),
            functorch_config.patch(unlift_effect_tokens=True),
        ):
            try:
                return aot_autograd(
                    fw_compiler=fw_compiler,
                    bw_compiler=bw_compiler,
                    inference_compiler=inference_compiler,
                    decompositions=decompositions,
                    partition_fn=partition_fn,
                    keep_inference_input_mutations=True,
                    cudagraphs=cudagraphs,
                    boxed_forward_device_index=forward_device,
                    ignore_shape_env=ignore_shape_env,
                )(model_, example_inputs_)
            except ShortenTraceback as e:
                # We will also shorten the traceback inside dynamo.
                # This is only useful if inductor is called directly with an FX graph.
                raise e.remove_dynamo_frames() from None  # see TORCHDYNAMO_VERBOSE=1
