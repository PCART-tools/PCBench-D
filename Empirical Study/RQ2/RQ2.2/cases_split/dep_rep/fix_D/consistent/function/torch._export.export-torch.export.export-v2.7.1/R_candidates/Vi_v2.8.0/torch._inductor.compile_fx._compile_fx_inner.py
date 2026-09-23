@time_and_log(attr="compilation time (in seconds)")
def _compile_fx_inner(
    gm: GraphModule,
    example_inputs: Sequence[InputType],
    **graph_kwargs: Unpack[_CompileFxKwargs],
) -> OutputCode:
    """
    Inductor API that compiles a single graph.

    If you change the argument list for this function, make sure you
    also update the call to save_args_for_compile_fx_inner below accordingly.
    """
    aot_mode: bool = V.aot_compilation

    # Clean up Compiled Triton Kernels per inductor compile, as the future objects
    # may not be valid for use after they are run/autotuned
    torch._inductor.async_compile.CompiledTritonKernels.cache_clear()

    if dynamo_utils.count_calls(gm.graph) == 0 and not aot_mode:
        # trigger the real recompilation for _LazyGraphModule before returning
        # the forward method.
        from torch._dynamo.utils import CompileEventLogLevel
        from torch.fx._lazy_graph_module import _LazyGraphModule

        _LazyGraphModule.force_recompile(gm)
        compile_id = torch._guards.CompileContext.current_compile_id()
        CompileEventLogger.log_instant_event(
            "backward no-op",
            metadata={"compile_id": compile_id},
            log_level=CompileEventLogLevel.PT2_COMPILE,
        )

        return make_boxed_func(gm.forward)

    static_input_idxs: Sequence[int] = graph_kwargs.setdefault("static_input_idxs", ())
    static_inputs_log.debug("static input idxs compile_fx_inner: %s", static_input_idxs)
    inputs_to_check = get_input_idxs_to_check(example_inputs, static_input_idxs)

    assert isinstance(next(iter(reversed(gm.graph.nodes))).args[0], (tuple, list)), (
        f"inductor can only compile FX graphs which return a tuple/list, but got {gm.graph}"
    )

    if graph_kwargs.get("cudagraphs") is None:
        graph_kwargs["cudagraphs"] = BoxedBool(config.triton.cudagraphs)
    if config.save_args:
        save_args_for_compile_fx_inner(
            gm,
            example_inputs,
            **graph_kwargs,
        )

    start = time.time()

    fx_graph_remote_cache = should_use_remote_fx_graph_cache()

    # Check if the registered backend(s) support caching.
    init_backend_registration()
    backends_support_caching = all(
        backend.supports_caching
        for backend in (
            get_wrapper_codegen_for_device(device.type, config.cpp_wrapper)
            for device in get_all_devices(gm)
        )
        if backend is not None
    )

    with dynamo_timed(
        "fx_codegen_and_compile", log_pt2_compile_event=True, log_waitcounter=True
    ):
        use_cache = (
            not config.force_disable_caches
            and (config.fx_graph_cache or fx_graph_remote_cache)
            and not aot_mode
            and backends_support_caching
        )
        local = config.fx_graph_cache
        remote = fx_graph_remote_cache
        set_feature_use("fx_cache", use_cache)

        log.debug(
            "FX cache status: use_cache=%s, local=%s, remote=%s, aot_mode=%s, force_disable_caches=%s",
            use_cache,
            local,
            remote,
            aot_mode,
            config.force_disable_caches,
        )

        # TODO: This is a hack purely to get some info to extract_tensor_metadata_for_cache_key,
        # figure out how to not have to modify example inputs
        for i, input in enumerate(example_inputs):
            if (
                isinstance(input, torch.Tensor)
                and is_gpu(input.device.type)
                and i in static_input_idxs
            ):
                input._is_inductor_static = True  # type: ignore[attr-defined]

        mb_compiled_graph: Optional[OutputCode] = None
        key_info = None
        cache_info = None
        remote_cache = None
        constants = CompiledFxGraphConstantsWithGm(gm)
        # TODO: this time will be slightly inconsistent with the one computed
        # in prepare_key/load_with_key, dump those settings of "cache_event_time"
        start_time = time.time_ns()

        if use_cache:
            (key_info, cache_info) = FxGraphCache.prepare_key(
                gm, example_inputs, graph_kwargs, inputs_to_check, remote
            )

            # Attempt a cache lookup
            if key_info is not None:
                key, debug_lines = key_info
                log.debug("FX cache key generated: %s", key)
                if remote:
                    remote_cache = FxGraphCache.get_remote_cache()
                    log.debug("Using remote FX cache")
                mb_compiled_graph, cache_info = FxGraphCache.load_with_key(
                    key,
                    debug_lines,
                    example_inputs,
                    local,
                    remote_cache,
                    is_backward=graph_kwargs.get("is_backward", False),
                    constants=constants,
                )
            else:
                log.debug("Failed to generate FX cache key")

        # CACHE BYPASS: Compile the graph, don't save it to the cache
        # (this can happen either because cache was disabled, or we
        # determined the input is uncacheable)
        if cache_info is None or cache_info["cache_state"] == "bypass":
            assert mb_compiled_graph is None
            log.debug(
                "FX cache bypass reason: %s",
                (
                    cache_info.get("cache_bypass_reason", "unknown")
                    if cache_info is not None
                    else "FX cache disabled or key generation failed"
                ),
            )
            mb_compiled_graph = fx_codegen_and_compile(
                gm, example_inputs, inputs_to_check, **graph_kwargs
            )

        # CACHE MISS: Compile the graph and save to cache
        elif cache_info["cache_state"] == "miss":
            assert mb_compiled_graph is None
            assert key_info is not None
            log.debug("FX cache miss, compiling and saving to cache")
            TritonBundler.begin_compile()
            try:
                mb_compiled_graph = fx_codegen_and_compile(
                    gm, example_inputs, inputs_to_check, **graph_kwargs
                )
                assert mb_compiled_graph is not None
                mb_compiled_graph._time_taken_ns = time.time_ns() - start_time
                cache_key, debug_lines = key_info
                mb_compiled_graph._fx_graph_cache_key = cache_key
                mb_compiled_graph._fx_graph_cache_debug_lines = debug_lines
                (
                    triton_bundle,
                    triton_bundler_meta,
                ) = TritonBundler.collect()
                mb_compiled_graph.set_triton_bundle(triton_bundle)
            except (ShortenTraceback, SkipFrame):
                raise
            except Exception as e:
                raise InductorError(e, currentframe()).with_traceback(
                    e.__traceback__
                ) from None
            finally:
                TritonBundler.end_compile()
            if triton_bundler_meta is not None:
                cache_info["triton_bundler_meta"] = str(triton_bundler_meta)
            cache_info["time_taken_ns"] = mb_compiled_graph._time_taken_ns
            log.debug("Saving compiled graph to FX cache with key: %s", cache_key)
            FxGraphCache._save_graph(
                cache_key,
                mb_compiled_graph,
                example_inputs,
                local,
                remote_cache,
            )

        # CACHE HIT: not much to really do, just make sure the cache key
        # is recorded on the graph
        else:
            assert cache_info["cache_state"] == "hit"
            assert mb_compiled_graph is not None
            assert key_info is not None
            (cache_key, debug_lines) = key_info
            log.debug("FX cache hit with key: %s", cache_key)
            mb_compiled_graph._fx_graph_cache_key = cache_key
            mb_compiled_graph._fx_graph_cache_debug_lines = debug_lines

        assert mb_compiled_graph is not None
        compiled_graph = mb_compiled_graph

        # Logging and observability: we log a single chromium event
        # and a tlparse log for every cache action.
        # In the event of a bypass, we also logged to the remote table earlier
        # with log_cache_bypass.
        cache_state = (
            cache_info["cache_state"] if cache_info is not None else "disabled"
        )
        # Here for grepping:
        # fx_graph_cache_hit
        # fx_graph_cache_miss
        # fx_graph_cache_bypass
        # fx_graph_cache_disabled
        CompileEventLogger.instant(
            f"fx_graph_cache_{cache_state}",
            metadata=cache_info or {},
            time_ns=start_time,
        )
        # Add event data about cache hits/miss
        # TODO: add remote cache get/put timings here too
        CompileEventLogger.pt2_compile(
            "inductor_compile",
            cache_state=cache_state,
            cache_event_time=start_time,
            key=cache_info.get("key") if cache_info else None,
            components=cache_info.get("components") if cache_info else None,
            cache_bypass_reason=(
                cache_info.get("cache_bypass_reason")
                if cache_info
                else "cache not enabled"
            ),
            remote_cache_enabled=remote,
            local_cache_enabled=local,
        )

        # Don't clog up the main tlparse output with disabled cache
        if cache_info is not None:
            trace_structured(
                "artifact",
                metadata_fn=lambda: {
                    "name": f"fx_graph_cache_{cache_state}",
                    "encoding": "json",
                },
                payload_fn=lambda: json.dumps(cache_info),
            )
        compiled_graph.post_compile(example_inputs, constants, graph_kwargs)

    log.debug("FX codegen and compilation took %.3fs", time.time() - start)

    # Dump provenance artifacts for debugging trace
    provenance_info = V.debug.log_inductor_triton_kernel_to_post_grad_node_info()
    # provenance_info might be None if config.trace.enabled is not set
    if provenance_info:
        (
            debug_info,
            node_mappings,
        ) = provenance_info
        trace_structured(
            "artifact",
            metadata_fn=lambda: {
                "name": "inductor_generated_kernel_to_post_grad_nodes",
                "encoding": "json",
            },
            payload_fn=lambda: json.dumps(debug_info),
        )
        trace_structured(
            "artifact",
            metadata_fn=lambda: {
                "name": "inductor_provenance_tracking_node_mappings",
                "encoding": "json",
            },
            payload_fn=lambda: json.dumps(node_mappings),
        )

    # This message is for printing overview information of inductor mm counts, shapes,etc after lowering
    if log.isEnabledFor(logging.INFO):
        mm_table_data = []
        for key, value in counters["aten_mm_info"].items():
            parts = key.split("_")
            if len(parts) < 3:
                # Unexpected format, show as-is
                mm_table_data.append([key, "-", "?", "?", "?", value])
                continue

            # Determine if this is a batched operation by checking the operation name
            name = "_".join(parts[:-4]) if len(parts) >= 4 else "_".join(parts[:-3])
            is_batched = name.endswith(("bmm", "baddbmm"))

            if is_batched and len(parts) >= 4:
                # Batched operation: last 4 parts are batch, m, n, k
                batch, m, n, k = parts[-4:]
                name = "_".join(parts[:-4])
                mm_table_data.append([name, batch, m, n, k, value])
            else:
                # Non-batched operation: last 3 parts are m, n, k
                m, n, k = parts[-3:]
                name = "_".join(parts[:-3])
                mm_table_data.append([name, "-", m, n, k, value])

        log.info("Overview info of inductor aten mms: ")
        log.info(
            "{:<30} | {:<20} | {:<20} | {:<20} | {:<20} | {:<20}".format(  # noqa: G001
                "Name", "B", "M", "N", "K", "Count"
            )
        )
        log.info("-" * 130)
        for row in mm_table_data:
            log.info("{:<30} | {:<20} | {:<20} | {:<20} | {:<20} | {:<20}".format(*row))  # noqa: G001
            log.info("-" * 130)

    # Not strictly necessary, but good to clean up straggling futures
    # that are unused to reclaim memory.
    torch._inductor.async_compile.CompiledTritonKernels.cache_clear()

    _step_logger()(
        logging.INFO,
        "torchinductor done compiling "
        f"{'BACKWARDS' if graph_kwargs['is_backward'] else 'FORWARDS'} "
        f"graph {graph_kwargs['graph_id']}",
    )
    return compiled_graph
