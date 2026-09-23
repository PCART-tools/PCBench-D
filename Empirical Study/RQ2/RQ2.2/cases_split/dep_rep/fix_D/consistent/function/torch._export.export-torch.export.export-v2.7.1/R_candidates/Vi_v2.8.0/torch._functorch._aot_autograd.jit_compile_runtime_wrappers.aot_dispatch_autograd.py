def aot_dispatch_autograd(
    flat_fn,
    flat_args: list[Any],
    aot_config: AOTConfig,
    *,
    fw_metadata: ViewAndMutationMeta,
) -> DispatchReturn:
    """
    Autograd logic. Generates a joint graph, partitions it, manipulates the input with various wrappers,
    and returns a wrapped torch.autograd.Function with a forward and backward.
    """
    wrappers = _create_wrappers_for_dispatch(needs_autograd=True)
    flat_fn, flat_args, fw_metadata = pre_compile(
        wrappers,
        flat_fn,
        flat_args,
        aot_config,
        fw_metadata=fw_metadata,
    )

    fw_metadata.deterministic = torch.are_deterministic_algorithms_enabled()
    with dynamo_timed("aot_trace_joint_graph", log_pt2_compile_event=True):
        fx_g, joint_inputs, maybe_subclass_meta = aot_dispatch_autograd_graph(
            flat_fn, flat_args, aot_config, fw_metadata=fw_metadata
        )

    # Copied from aot_dispatch_autograd_graph.
    disable_amp = torch._C._is_any_autocast_enabled()
    joint_graph_str = None
    if aot_config.enable_log:
        aot_joint_log.info(
            "%s",
            lazy_format_graph_code(
                "Joint graph",
                fx_g,
                aot_config.aot_id,
                include_stride=True,
                include_device=True,
                colored=True,
            ),
        )
        joint_graph_str = fx_g.print_readable(
            print_output=False, include_stride=True, include_device=True
        )
        trace_structured(
            "aot_joint_graph",
            payload_fn=lambda: joint_graph_str,
        )

    with torch.no_grad():
        inner_meta = (
            fw_metadata
            if maybe_subclass_meta is None
            else maybe_subclass_meta.fw_metadata
        )
        with track_graph_compiling(aot_config, "joint"):
            # See Note: [Partitioner handling for Subclasses, Part 1]
            # See Note: [Recomputing subclass mutation handling]
            mutated_inp_runtime_indices = (
                compute_inner_mutated_inp_indices_from_subclass_meta(
                    fw_metadata, inner_meta
                )
            )
            num_tokens = len(fw_metadata.tokens)
            num_mutated_inp_runtime_indices = len(mutated_inp_runtime_indices)
            num_inner_fwd_outputs = (
                num_mutated_inp_runtime_indices
                + inner_meta.num_outputs
                + inner_meta.num_intermediate_bases
                + inner_meta.num_outputs_rng_offset
                + num_tokens  # See Note [Side-Effectful Tokens in AOTAutograd]
            )
            fake_mode = detect_fake_mode()
            fx_g = run_joint_graph_passes_on_hops(fx_g, joint_inputs, aot_config)

            # TODO(anijain2305) - Add tensorify_python_scalars to the HOP graph passes.
            if fake_mode is not None and fake_mode.shape_env is not None:
                tensorify_python_scalars(fx_g, fake_mode.shape_env, fake_mode)

            static_lifetime_input_indices = fw_metadata.static_input_indices
            fw_module, bw_module = aot_config.partition_fn(
                fx_g,
                joint_inputs,
                num_fwd_outputs=num_inner_fwd_outputs,
                static_lifetime_input_indices=static_lifetime_input_indices,
            )
            rng_states = [
                n
                for n in fw_module.graph.find_nodes(op="placeholder")
                if "fwd_rng_state" in n.name
            ]
            fw_metadata.num_graphsafe_rng_states = len(rng_states)
            if rng_states:
                fw_metadata.graphsafe_rng_state_index = (
                    rng_states[0].meta["val"].device.index
                )

            # See Note [Side-Effectful Tokens in AOTAutograd]
            if config.unlift_effect_tokens and (
                num_tokens > 0 or fw_metadata.num_backward_tokens > 0
            ):
                unlift_tokens(fw_module, fw_metadata, aot_config, bw_module)

                num_inner_fwd_outputs -= num_tokens
                joint_inputs = (
                    joint_inputs[0][num_tokens:],
                    joint_inputs[1],
                )

            maybe_inline_graph_saved_tensors_hooks(
                fw_module,
                bw_module,
                num_inner_fwd_outputs,
                inner_meta,
                aot_config,
                fw_metadata.static_input_indices,
            )
            static_lifetime_input_indices = fw_metadata.static_input_indices

            fw_outs = next(iter(fw_module.graph.find_nodes(op="output"))).args[0]
            # we only need to bookkeep the symints that are saved for bw, not any symints
            # the user forward might have returned in its own output
            fw_outs_saved_for_bw = fw_outs[num_inner_fwd_outputs:]
            num_fw_outs_saved_for_bw = len(fw_outs_saved_for_bw)
            symint_outs_saved_for_bw = []
            for idx, node in enumerate(fw_outs_saved_for_bw):
                if is_sym_node(node):
                    symint_outs_saved_for_bw.append(node)
                elif (
                    isinstance(node, torch.fx.Node)
                    and "val" in getattr(node, "meta", {})
                    and isinstance(node.meta["val"], FakeTensor)
                ):
                    # record dynamic tensor activations
                    dynamic_dims: set[int] = {
                        dim
                        for dim, size in enumerate(node.meta["val"].shape)
                        if not isinstance(size, int)
                    }
                    if dynamic_dims:
                        fw_metadata.dynamic_saved_tensors_idxs[idx] = dynamic_dims

            fw_metadata.num_symints_saved_for_bw = len(symint_outs_saved_for_bw)
            inner_meta.num_symints_saved_for_bw = len(symint_outs_saved_for_bw)
            num_symints_saved_for_bw = len(symint_outs_saved_for_bw)
            if torch._functorch.config.donated_buffer:
                fw_metadata.bw_donated_idxs = collect_bw_donated_buffer_idxs(
                    fw_module,
                    bw_module,
                    inner_meta,
                )
                inner_meta.bw_donated_idxs = fw_metadata.bw_donated_idxs

        if aot_config.enable_log:
            trace_structured(
                "artifact",
                metadata_fn=lambda: {
                    "name": "torch._functorch.config",
                    "encoding": "string",
                },
                payload_fn=lambda: torch._functorch.config.get_config_copy(),
            )
            aot_graphs_log.info(
                "aot_config id: %s, fw_metadata=%s, inner_meta=%s",
                str(aot_config.aot_id),
                str(fw_metadata),
                str(inner_meta),
            )

        # Note [Detaching inputs that never need gradients]
        # See https://github.com/pytorch/pytorch/issues/97745
        # Suppose we have a function like this that we want to compile:
        #
        # def f(x, y):
        #     return torch.mul(x, y.detach())
        #
        # What gradients should we compute for x and y?
        # By default, AOTAutograd will compute a gradient for **every** input that requires gradients,
        # and so we'll compute:
        #    x_grad_input = y
        #    y_grad_input = None
        # Does this preserve the semantics of eager mode?
        # Unfortunately, no.
        # Doing the above will cause autograd to **continue** to backprop the autograd tape
        # that was generated from constructing y.
        #
        # This is **different** from what would have happened in eager mode.
        # In eager mode, if we backprop through the output of this function, autograd will only traverse
        # the bit of the autograd tape corresponding to "x".
        # In particular, if a user had previously backpropped through y's autograd tape,
        # And then they try to backprop through the output of the above function,
        # then we'll hit the dreaded "Trying to backward through the graph a second time" error.
        #
        # You might think: If autograd sees that a gradient is None, shouldn't it stop early,
        # instead of continuing the backprop through the ancestors of that node in the graph?
        #
        # Autograd has two passes:
        # (1) a first pass that traverses the autograd graph and figures out which nodes need to be executed
        # (2) a second pass that actually goes ahead and executes each node when it becomes ready,
        #     propagating gradients
        # By the time we're executing a node and we see that it produces a None, the set of nodes to execute
        # is already locked-in.
        #
        # The fix: instead, we can recognize statically that the graph we're compiling will never contribute
        # gradients to y, and prevent autograd from trying to traverse y's autograd tape at all.
        # We can do this by manually detach'ing y before sending it through the `CompiledFunction`.
        #
        # Note that this solution is not bulletproof.
        # It's possible to construct a case where eager may or may not have have tried to autograd through y,
        # depending on the actual grad_outputs that were passed in during the backward.
        # There is no easy fix for this: the simplest fix would be to run with `retain_graph=True`,
        # allowing autograd to re-use the graph.
        #
        # An example of this case is:
        # def f(x):
        #     return x.detach() * 2, x * 3
        # If we were to only backprop through outs[0], in eager, we would stop
        # If we backward only on the first output, we shouldn't send a grad through x.
        # But the custom autograd function doesn't know that: it will materialize zero grads for x * 3
        # and we will end up with a zero grad at x.
        # If we later backprop through the second output, this will also require backprop'ing through x.
        # Meaning we'll need to use `retain_graph=True` to be able to backprop through x the second time.
        _indices_of_inps_to_detach: list[int] = []

        # reversed() since we expect output at end of graph
        bw_output = next(reversed(bw_module.graph.find_nodes(op="output")))
        bw_outs: Sequence[torch.fx.Node] = bw_output.args[0]  # type: ignore[assignment]

        # TODO: we should apply the below "detach inputs if their gradients are statically known to be None"
        # optimization even if we have subclass inputs/outputs (we do not handle this today).
        # Computing which our our inputs get None gradients is a bit more complicated,
        # if any of our inputs are subclasses. Why?
        # (a) we need to make sure that we call .detach() on the input subclasses, since autograd sees subclasses.
        # (b) The grad_outputs that we AOT computed in our backward graph are the desugared tensor tensors,
        #     so we need to figure out which subclass fw inputs they map to.
        if maybe_subclass_meta is None:
            num_backward_tokens: int = inner_meta.num_backward_tokens
            assert (
                len(bw_outs)
                == len(fw_metadata.input_info)
                + inner_meta.num_outputs_rng_offset
                + num_backward_tokens
            )
            bw_outs_no_rng_no_tokens = bw_outs
            if (inner_meta.num_outputs_rng_offset + num_backward_tokens) > 0:
                bw_outs_no_rng_no_tokens = bw_outs[
                    : -(inner_meta.num_outputs_rng_offset + num_backward_tokens)
                ]
            assert len(bw_outs_no_rng_no_tokens) == len(fw_metadata.input_info)

            for i, (bw_out) in enumerate(bw_outs_no_rng_no_tokens):
                # If our input experiences a metadata mutation inside the graph (e.g. set_()),
                # we *must* not detach, otherwise it will be the detach'd input that gets the metadata mutation
                metadata_mutation_in_graph = (
                    fw_metadata.input_info[i].mutation_type
                    == MutationType.MUTATED_IN_GRAPH
                    and fw_metadata.input_info[i].mutates_storage_metadata
                )
                is_non_leaf = (
                    fw_metadata.input_info[i].requires_grad
                    and not fw_metadata.input_info[i].is_leaf
                )
                if bw_out is None and not metadata_mutation_in_graph and is_non_leaf:
                    _indices_of_inps_to_detach.append(i)

        fw_module_str = None
        bw_module_str = None
        if aot_config.enable_log:
            aot_graphs_log.info(
                "%s",
                lazy_format_graph_code(
                    "Forward graph",
                    fw_module,
                    aot_config.aot_id,
                    include_stride=True,
                    include_device=True,
                    colored=True,
                ),
            )
            aot_graphs_log.info(
                "%s",
                lazy_format_graph_code(
                    "Backward graph",
                    bw_module,
                    aot_config.aot_id,
                    include_stride=True,
                    include_device=True,
                    colored=True,
                ),
            )
            fw_module_str = fw_module.print_readable(
                print_output=False, include_stride=True, include_device=True
            )
            bw_module_str = bw_module.print_readable(
                print_output=False, include_stride=True, include_device=True
            )

            trace_structured(
                "artifact",
                metadata_fn=lambda: {
                    "name": "aot_forward_graph_fw_metadata",
                    "encoding": "string",
                },
                payload_fn=lambda: dataclass_repr(fw_metadata),
            )
            if maybe_subclass_meta is not None:
                trace_structured(
                    "artifact",
                    metadata_fn=lambda: {
                        "name": "aot_forward_graph_fw_subclass_metadata",
                        "encoding": "string",
                    },
                    payload_fn=lambda: dataclass_repr(maybe_subclass_meta),
                )

            trace_structured(
                "aot_forward_graph",
                payload_fn=lambda: fw_module_str,
            )
            trace_structured(
                "aot_backward_graph",
                payload_fn=lambda: bw_module_str,
            )

        # AMP is already traced out in joint graph. we do not wish to reapply it accidentally
        # in the compiler.
        with track_graph_compiling(aot_config, "forward"), torch._C._DisableAutocast():
            # flat_args at this point might still be subclasses-
            # make sure to pass the unwrapped fake tensors into the compiler!
            adjusted_flat_args = joint_inputs[0]

            fakified_out_wrapper = FakifiedOutWrapper()
            (
                fw_module,
                adjusted_flat_args,
                fw_metadata,
            ) = fakified_out_wrapper.pre_compile(
                fw_module, adjusted_flat_args, aot_config, fw_metadata=fw_metadata
            )

            functionalized_rng_wrapper = FunctionalizedRngRuntimeWrapper(
                return_new_outs=False
            )

            if rng_states:
                index = fw_metadata.graphsafe_rng_state_index
                assert index is not None
                rng_states = [
                    get_cuda_generator_meta_val(index)
                    for _ in range(fw_metadata.num_graphsafe_rng_states)
                ]
                adjusted_flat_args.extend(rng_states)  # type: ignore[arg-type]

            (
                fw_module,
                adjusted_flat_args,
                fw_metadata,
            ) = functionalized_rng_wrapper.pre_compile(
                fw_module, adjusted_flat_args, aot_config, fw_metadata=fw_metadata
            )
            if tracing_context := torch._guards.TracingContext.try_get():
                tracing_context.fw_metadata = inner_meta

            with TracingContext.report_output_strides() as fwd_output_strides:
                compiled_fw_func = aot_config.fw_compiler(fw_module, adjusted_flat_args)

            if not getattr(compiled_fw_func, "_boxed_call", False):
                compiled_fw_func = make_boxed_func(compiled_fw_func)

            if fakified_out_wrapper.needs_post_compile:
                fakified_out_wrapper.set_fwd_output_strides(fwd_output_strides)

            compiled_fw_func = EffectTokensWrapper().post_compile(
                compiled_fw_func,
                aot_config,
                runtime_metadata=fw_metadata,
            )

            compiled_fw_func = AOTDispatchSubclassWrapper(
                fw_only=None,
                trace_joint=False,
                maybe_subclass_meta=maybe_subclass_meta,
                num_fw_outs_saved_for_bw=num_fw_outs_saved_for_bw,
            ).post_compile(
                compiled_fw_func,
                aot_config,  # not used
                runtime_metadata=fw_metadata,
            )

            compiled_fw_func = functionalized_rng_wrapper.post_compile(
                compiled_fw_func, aot_config, runtime_metadata=fw_metadata
            )
            compiled_fw_func = fakified_out_wrapper.post_compile(
                compiled_fw_func,
                aot_config,
                runtime_metadata=fw_metadata,
            )

        # NB: It's important to compile backwards ahead of time, as this may
        # add extra guards which we need to apply to the Dynamo cache at
        # forwards
        with track_graph_compiling(aot_config, "backward"), torch._C._DisableAutocast():
            placeholder_list = fx_placeholder_vals(bw_module)

            forward_saved_for_backwards_strides = None
            if fwd_output_strides is not None:
                forward_saved_for_backwards_strides = fwd_output_strides[
                    inner_meta.tensors_saved_for_backwards_slice
                ]

            # saved activations can have different stride to eager if
            # the compiler does layout optimization. We should restride the
            # tensor passed in for compiling the backward graph using the
            # saved tensor's stride.
            for i in range(len(placeholder_list)):
                ph_arg = placeholder_list[i]
                if not isinstance(ph_arg, torch.Tensor):
                    continue

                if forward_saved_for_backwards_strides is None:
                    continue

                real_stride = None
                # Per all_args calling convention
                j = i - num_symints_saved_for_bw
                if 0 <= j < len(forward_saved_for_backwards_strides):
                    real_stride = forward_saved_for_backwards_strides[j]
                if real_stride is None:
                    continue

                # Comparing ph_arg.stride() with real_stride directly may
                # cause dynamic dimensions in ph_arg being specialized to static
                # value. Using the hints to avoid that.
                if _get_symint_hints(ph_arg.stride()) != real_stride:
                    # Note that here we use the stride of the real tensor to
                    # restride a FakeTensor. This does not cause trouble
                    # for dynamic shape since this code path only get
                    # executed if layout optimization is enabled. And we
                    # disable layout optimization for dynamic shape right
                    # now.
                    #
                    # A solution that decide stride order based on real
                    # tensor's stride and then apply that stride order to
                    # the FakeTensor does not work smoothly since some
                    # tensor's layout is not 'dense'. E.g. mixnet_l has a
                    # tensor with size [8, 64, 112, 112] and strides
                    # (2408448, 1, 21504, 192). The solution mentioned will
                    # decide a stride of (802816, 1, 7168, 64) for this
                    # tensor which is wrong.
                    placeholder_list[i] = ph_arg.as_strided(ph_arg.size(), real_stride)

            compiled_bw_func = None
            if num_symints_saved_for_bw > 0:
                try:
                    # See Note: [Backward graph lazy lowering]
                    with torch._subclasses.fake_tensor.unset_fake_temporarily():
                        # If bw_module contains lifted constants, they will be real tensors stored as
                        # GraphModule. Deepcopying tensors under fake mode is not supported and will
                        # raise when attempting to set storage.
                        bw_module_copy = copy.deepcopy(bw_module)
                    compiled_bw_func = aot_config.bw_compiler(
                        bw_module_copy, placeholder_list
                    )
                    del bw_module_copy
                except Exception as e:
                    exc = e
                    trace_structured(
                        "artifact",
                        metadata_fn=lambda: {
                            "name": "eager_compile_backwards_failure",
                            "encoding": "string",
                        },
                        payload_fn=lambda: "\n".join(
                            traceback.format_exception(
                                type(exc), exc, exc.__traceback__
                            )
                        ),
                    )
                    log.warning(
                        "failed to eagerly compile backwards for dynamic, suppressing in case backwards not needed",
                        exc_info=True,
                    )
            # Compiled autograd will run the bw_module in the backward pass,
            # so recompilation need happen anyway if the backward pass is ever
            # called.
            #
            # The reason we do the GraphModule recompilation here is because
            # the lazy recompilation will cause issue in the backward pass
            # with compiled autograd.
            #
            # Do the _LazyGraphModule.force_recompile here rather than when
            # bw_module is first generated by the partitioner because the bw_module.recompile
            # may be called in some code path later and cause the _LazyGraphModule.forward
            # becomes the lazy version again. One example is when dynamic shape is enabled
            # upfront, the bw_compiler will be called above which can cause extra
            # graph module recompilation on bw_module.
            if torch._dynamo.compiled_autograd.in_compiled_autograd_region:
                from torch.fx._lazy_graph_module import _LazyGraphModule

                _LazyGraphModule.force_recompile(bw_module)

    saved_context = TracingContext.try_get()
    saved_compile_context = CompileContext.try_get()

    backward_state_indices = [
        idx for idx, x in enumerate(flat_args) if isinstance(x, BackwardState)
    ]
    assert len(backward_state_indices) <= 1

    lazy_backward_info = AutogradLazyBackwardCompileInfo(
        bw_module,
        placeholder_list,
        saved_context,
        saved_compile_context,
    )

    make_runtime_safe(fw_metadata, maybe_subclass_meta)

    try_save_cache_entry: Optional[Callable] = None

    if aot_config.cache_info is not None:
        forward_time_taken_ns = time.time_ns() - aot_config.cache_info.start_time_ns

        # NB: aot_config here is technically not needed as an argument: we could just
        # close over aot_config.cache_info, since aot_config never changes.
        # But closing over random variables is confusing IMO, so I'm leaving it.
        def try_save_cache_entry(  # noqa: F811
            compiled_bw_func: Callable,
            bw_module: torch.fx.GraphModule,
            _fw_metadata: ViewAndMutationMeta,
            aot_config: AOTConfig,
        ):
            fw_key = getattr(compiled_fw_func, "_fx_graph_cache_key", None)
            bw_key = getattr(compiled_bw_func, "_fx_graph_cache_key", None)
            cache_info = aot_config.cache_info
            if cache_info is not None and fw_key and bw_key:
                assert forward_time_taken_ns is not None
                # TODO: technically, AOTAutograd does a *little* bit of post processing work
                # in the backward that isn't measured here. But it's small enough that it's not worth
                # the complexity of threading a bunch of times through the code, so we
                # use the compiled_bw_func's inductor compile time instead.
                # It's possible this changes in the future, in which case we should
                # update backward_time_taken_ns to be more inclusive
                backward_time_taken_ns = getattr(compiled_bw_func, "_time_taken_ns", 0)

                aot_forward_graph_str: Optional[str] = fw_module_str
                aot_backward_graph_str: Optional[str] = bw_module_str
                aot_joint_graph_str: Optional[str] = joint_graph_str
                guards_expr = AOTAutogradCache.generate_guards_expression(cache_info)

                entry = AOTAutogradCache.make_entry(
                    compiled_fw_func,  # type: ignore[arg-type]
                    compiled_bw_func,  # type: ignore[arg-type]
                    aot_joint_graph_str,
                    aot_forward_graph_str,
                    aot_backward_graph_str,
                    _fw_metadata,
                    wrappers,
                    maybe_subclass_meta,
                    num_fw_outs_saved_for_bw,
                    _indices_of_inps_to_detach,
                    forward_time_taken_ns,
                    backward_time_taken_ns,
                    sanitized_aot_config=sanitize_aot_config(aot_config),
                    guards_expr=guards_expr,
                    backward_state_indices=backward_state_indices,
                    num_symints_saved_for_bw=num_symints_saved_for_bw,
                    serialized_bw_module=serialize_graph_module(bw_module),
                )
                remote = should_use_remote_autograd_cache()
                AOTAutogradCache.save(cache_info.cache_key, entry, remote)

        if compiled_bw_func is not None:
            # If we already compiled the backward, we save its cache entry now
            try_save_cache_entry(compiled_bw_func, bw_module, fw_metadata, aot_config)
            try_save_cache_entry = None

    compiled_fn = AOTDispatchAutograd.post_compile(
        compiled_fw_func,
        compiled_bw_func,
        maybe_subclass_meta,
        num_symints_saved_for_bw,
        backward_state_indices,
        disable_amp,
        _indices_of_inps_to_detach,
        lazy_backward_info,
        aot_config,
        fw_metadata=fw_metadata,
        try_save_cache_entry=try_save_cache_entry,
    )

    if config.debug_assert:
        flat_requires_grad: list[Optional[bool]] = [
            a.requires_grad if isinstance(a, Tensor) else None for a in flat_args
        ]
        compiled_fn = DebugAssertWrapper(
            flat_requires_grad=flat_requires_grad
        ).post_compile(compiled_fn, aot_config, runtime_metadata=fw_metadata)

    compiled_fn = post_compile(
        wrappers,
        compiled_fn,
        aot_config,
        runtime_metadata=fw_metadata,
    )
    return compiled_fn
