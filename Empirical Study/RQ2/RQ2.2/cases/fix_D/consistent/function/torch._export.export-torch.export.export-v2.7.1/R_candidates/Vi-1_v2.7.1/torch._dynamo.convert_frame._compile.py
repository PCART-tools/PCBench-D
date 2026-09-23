def _compile(
    code: CodeType,
    globals: dict[str, object],
    locals: dict[str, object],
    builtins: dict[str, object],
    closure: tuple[CellType],
    compiler_fn: CompilerFn,
    one_graph: bool,
    export: bool,
    export_constraints: Optional[typing.Never],
    hooks: Hooks,
    cache_entry: Optional[CacheEntry],
    cache_size: CacheSizeRelevantForFrame,
    frame: Optional[DynamoFrameType] = None,
    frame_state: Optional[dict[str, Union[int, FrameStateSizeEntry]]] = None,
    *,
    compile_id: CompileId,
    skip: int = 0,
) -> ConvertFrameReturn:
    from torch.fx.experimental.validator import (
        bisect,
        BisectValidationException,
        translation_validation_enabled,
        ValidationException,
    )

    # Only nonlocal defs here please!
    # Time spent compiling this frame before restarting or failing analysis
    dynamo_time_before_restart: float = 0.0
    output: Optional[OutputGraph] = None
    tracer: Optional[InstructionTranslator] = None

    tf_mode_stack: list[torch.overrides.TorchFunctionMode] = (
        torch.overrides._get_current_function_mode_stack()
    )

    @preserve_global_state
    def transform(
        instructions: list[Instruction], code_options: dict[str, object]
    ) -> None:
        nonlocal output
        nonlocal tracer
        speculation_log.restart()
        exn_vt_stack = ExceptionStack()
        tracer = InstructionTranslator(
            instructions,
            code,
            locals,
            globals,
            builtins,
            closure,
            tf_mode_stack,
            code_options,
            compiler_fn,
            one_graph,
            export,
            export_constraints,
            frame_state=frame_state,
            speculation_log=speculation_log,
            exn_vt_stack=exn_vt_stack,
            distributed_state=distributed_state,
        )

        try:
            with tracing(tracer.output.tracing_context), tracer.set_current_tx():
                tracer.run()
        except exc.UnspecializeRestartAnalysis:
            speculation_log.clear()
            raise
        except (
            exc.SpeculationRestartAnalysis,
            exc.TensorifyScalarRestartAnalysis,
            exc.SkipFrame,
        ):
            raise
        except Exception:
            if translation_validation_enabled():
                bisect(tracer.output.shape_env)
            raise
        finally:
            tracer.output.call_cleanup_hooks()

        output = tracer.output
        assert output is not None
        assert output.output_instructions
        instructions[:] = output.output_instructions
        code_options.update(output.code_options)
        propagate_inst_exn_table_entries(instructions)
        check_inst_exn_tab_entries_valid(instructions)
        instructions[:] = remove_pointless_jumps(remove_dead_code(instructions))

    @compile_time_strobelight_meta(phase_name="compile_inner")
    def compile_inner(
        code: CodeType,
        one_graph: bool,
        hooks: Hooks,
        transform: Callable[[list[Instruction], dict[str, Any]], Any],
    ) -> ConvertFrameReturn:
        with contextlib.ExitStack() as stack:
            stack.enter_context(
                dynamo_timed(
                    "_compile.compile_inner",
                    phase_name="entire_frame_compile",
                    dynamo_compile_column_us="dynamo_cumulative_compile_time_us",
                )
            )
            stack.enter_context(
                _WaitCounter("pytorch.wait_counter.dynamo_compile").guard()
            )
            stack.enter_context(torch._dynamo.callback_handler.install_callbacks())
            stack.enter_context(CompileTimeInstructionCounter.record())
            return _compile_inner(code, one_graph, hooks, transform)

        return (
            ConvertFrameReturn()
        )  # dead, but see https://github.com/python/mypy/issues/7577

    @maybe_cprofile
    def _compile_inner(
        code: CodeType,
        one_graph: bool,
        hooks: Hooks,
        transform: Callable[[list[Instruction], dict[str, Any]], Any],
    ) -> ConvertFrameReturn:
        nonlocal dynamo_time_before_restart
        last_attempt_start_time = start_time = time.time()

        def log_bytecode(
            prefix: str, name: str, filename: str, line_no: int, code: CodeType
        ) -> None:
            if bytecode_log.isEnabledFor(logging.DEBUG):
                bytecode_log.debug(
                    format_bytecode(prefix, name, filename, line_no, code)
                )

        log_bytecode(
            "ORIGINAL BYTECODE",
            code.co_name,
            code.co_filename,
            code.co_firstlineno,
            code,
        )

        out_code = None
        for attempt in itertools.count():
            CompileContext.get().attempt = attempt
            try:
                out_code = transform_code_object(code, transform)
                break
            except exc.RestartAnalysis as e:
                if not isinstance(e, exc.TensorifyScalarRestartAnalysis):
                    TensorifyState.clear()
                log.info(
                    "Restarting analysis due to %s",
                    LazyString(format_traceback_short, e.__traceback__),
                )
                # If restart reason is None just log the type of the exception
                restart_reasons.add(e.restart_reason or str(type(e)))
                # We now have a new "last attempt", reset the clock
                last_attempt_start_time = time.time()
                if attempt > 100:
                    unimplemented_v2(
                        gb_type="Excessive RestartAnalysis() calls",
                        context="",
                        explanation="Dynamo attempted to trace the same frame 100+ times. "
                        "Giving up on compiling as the compile time tradeoff is likely not "
                        "worth the performance gain.",
                        hints=[],
                    )
            except exc.SkipFrame as e:
                if not isinstance(e, exc.TensorifyScalarRestartAnalysis):
                    TensorifyState.clear()
                log.debug(
                    "Skipping frame %s %s \
                    %s %s",
                    e,
                    code.co_name,
                    code.co_filename,
                    code.co_firstlineno,
                )
                if one_graph:
                    log.debug("No graph captured with one_graph=True")
                return ConvertFrameReturn()

        assert distributed_state is None or distributed_state.all_states is not None, (
            "compiler collective wasn't run before compilation completed"
        )

        assert out_code is not None
        log_bytecode(
            "MODIFIED BYTECODE",
            code.co_name,
            code.co_filename,
            code.co_firstlineno,
            out_code,
        )

        for hook in _bytecode_hooks.values():
            hook_output = hook(code, out_code)
            if hook_output is not None:
                out_code = hook_output

        orig_code_map[out_code] = code
        output_codes.add(out_code)
        dynamo_time_before_restart = last_attempt_start_time - start_time
        assert output is not None

        # Tests for new code objects.
        # The rationale for these tests can be found in torch/csrc/dynamo/eval_frame.c
        # Only test once the code object is created.
        # They are not tested during runtime.

        def count_args(code: CodeType) -> int:
            import inspect

            return (
                code.co_argcount
                + code.co_kwonlyargcount
                + bool(code.co_flags & inspect.CO_VARARGS)
                + bool(code.co_flags & inspect.CO_VARKEYWORDS)
            )

        assert out_code is not None

        total_argcount_old = count_args(code)
        total_argcount_new = count_args(out_code)
        msg = "arg mismatch: "
        msg += f"old code object has args {code.co_varnames[:total_argcount_old]}, "
        msg += f"new code object has args {out_code.co_varnames[:total_argcount_new]}"
        assert (
            code.co_varnames[:total_argcount_old]
            == out_code.co_varnames[:total_argcount_new]
        ), msg

        msg = "free var mismatch: "
        msg += f"old code object has free var {code.co_freevars}, "
        msg += f"new code object has free var {out_code.co_freevars}"
        assert code.co_freevars == out_code.co_freevars, msg

        msg = "cell var mismatch: "
        msg += f"old code object has cell var {code.co_cellvars}, "
        msg += f"new code object has cell var {out_code.co_cellvars}"
        assert code.co_cellvars == out_code.co_cellvars, msg

        # Skipping Dynamo on a frame without any extracted graph.
        # This does not affect eager functionality. But this is necessary
        # for export for cases where Dynamo-reconstructed bytecode can create
        # new function frames, confusing export in thinking that there
        # are extra graphs now.

        if output.export and output.is_empty_graph():
            return ConvertFrameReturn()

        assert output.guards is not None
        CleanupManager.instance[out_code] = output.cleanups
        nonlocal cache_entry
        check_fn = CheckFunctionManager(
            code,
            output,
            cache_entry,
            hooks.guard_fail_fn if hooks else None,
        )

        compile_id_str = str(compile_id) if compile_id is not None else "Unknown"
        annotation_str = "Torch-Compiled Region: " + compile_id_str
        guarded_code = GuardedCode(
            out_code,
            check_fn.guard_manager,  # type: ignore[arg-type]
            compile_id,
            annotation_str,
        )

        if not output.is_empty_graph() and hooks.guard_export_fn is not None:
            # We should not run the guard_export_fn when Dynamo does not
            # generate any graph. This can happen in export when TorchDynamo
            # generated bytecode has some reconstruction logic for mutated
            # variables which can trigger TorchDynamo on the children frames but
            # they are benign and do not generate any new graphs.
            hooks.guard_export_fn(output.guards)

        return wrap_guarded_code(guarded_code)

    metrics_context = get_metrics_context()
    with (
        _use_lazy_graph_module(config.use_lazy_graph_module),
        compile_context(CompileContext(compile_id)),
        chromium_event_timed(
            "dynamo", reset_event_log_on_exit=True, log_pt2_compile_event=True
        ),
        metrics_context,
    ):
        restart_reasons: set[str] = set()
        # This is shared across restarts
        speculation_log = SpeculationLog()
        if compile_pg := get_compile_pg():
            distributed_state = DistributedState(compile_pg, LocalState())
        else:
            distributed_state = None

        # Check recompilations
        recompile_reason: Optional[str] = None
        if is_recompilation(cache_size) and frame:
            reasons = get_and_maybe_log_recompilation_reasons(cache_entry, frame)
            recompile_reason = (
                "Unable to find recompilation reasons" if not reasons else reasons[0]
            )
        metrics_context.update_outer({"recompile_reason": recompile_reason})

        exceeded, limit_type = exceeds_recompile_limit(cache_size, compile_id)
        if exceeded:

            def format_func_info(code: CodeType) -> str:
                return f"'{code.co_name}' ({code.co_filename}:{code.co_firstlineno})"

            log.warning(
                "torch._dynamo hit config.%s (%s)\n"
                "   function: %s\n"
                "   last reason: %s\n"
                'To log all recompilation reasons, use TORCH_LOGS="recompiles".\n'
                "To diagnose recompilation issues, see %s.",
                limit_type,
                getattr(config, limit_type),
                format_func_info(code),
                recompile_reason,
                troubleshooting_url,
            )
            if config.fail_on_recompile_limit_hit:
                raise FailOnRecompileLimitHit(
                    f"{limit_type} reached, because fail_on_recompile_limit_hit = True this is a HARD failure"
                )
            elif one_graph:
                raise FailOnRecompileLimitHit(
                    f"{limit_type} reached with one_graph=True. Excessive recompilations can degrade "
                    "performance due to the compilation overhead of each recompilation. To monitor "
                    "recompilations, enable TORCH_LOGS=recompiles. If recompilations are expected, consider "
                    "increasing torch._dynamo.config.cache_size_limit to an appropriate value."
                )
            elif justknobs_check(
                "pytorch/compiler:skip_code_recursive_on_recompile_limit_hit"
            ):
                raise RecompileLimitExceeded(f"{limit_type} reached")
            else:
                # do not recursively skip frames
                unimplemented_v2(
                    gb_type="Dynamo cache limit exceeded",
                    context=f"Limit type: {limit_type}",
                    explanation="Dynamo attempted to recompile the code object too many times, "
                    f"exceeding the {limit_type} cache size limit."
                    "Giving up on compiling as the compile time tradeoff is likely not "
                    "worth the performance gain.",
                    hints=[],
                )

        log.debug(
            "torchdynamo start compiling %s %s:%s, stack (elided %s frames):\n%s",
            code.co_name,
            code.co_filename,
            code.co_firstlineno,
            skip + 2,
            # -2: omit current frame, omit contextlib decorator
            "".join(CapturedTraceback.extract(skip=2 + skip).format()),
        )
        # -4: -2 as above, plus trace_structured frames
        #
        # NB: the frame looks like this:
        #
        # # handled by skip argument
        # torch/_dynamo/convert_frame.py:1069 in catch_errors
        # torch/_dynamo/convert_frame.py:910 in _convert_frame
        # torch/_dynamo/convert_frame.py:464 in _convert_frame_assert
        # torch/_utils_internal.py:70 in wrapper_function
        #
        # # 2 current frame and context lib
        # env/lib/python3.10/contextlib.py:79 in inner
        # torch/_dynamo/convert_frame.py:776 in _compile
        #
        # # 2 extra here
        # torch/_logging/_internal.py:1064 in trace_structured
        # torch/_dynamo/convert_frame.py:780 in <lambda>
        convert_frame_intern = structured.intern_string(__file__)
        # Initialize the ChromiumEventLogger on start
        torch._logging.trace_structured(
            "dynamo_start",
            lambda: {
                "stack": list(
                    itertools.takewhile(
                        lambda f: f["filename"] != convert_frame_intern,
                        structured.from_traceback(
                            CapturedTraceback.extract(skip=4 + skip).summary()
                        ),
                    )
                )
                + [
                    {
                        "line": code.co_firstlineno,
                        "name": code.co_name,
                        "filename": structured.intern_string(code.co_filename),
                    }
                ]
            },
        )
        start_time_ns = time.time_ns()
        fail_type: Optional[str] = None
        fail_reason: Optional[str] = None
        fail_user_frame_filename: Optional[str] = None
        fail_user_frame_lineno: Optional[int] = None
        torch._dynamo.utils.ReinplaceCounters.clear()
        guarded_code = None
        try:
            guarded_code = compile_inner(code, one_graph, hooks, transform)

            # NB: We only put_code_state in success case.  Success case here
            # does include graph breaks; specifically, if a graph break still
            # resulted in a partially compiled graph, we WILL return here.  An
            # Unsupported exception will only bubble to the top level if we
            # are unable to compile the frame at all.  In this case, there's
            # no point in uploading the code state, because we will always
            # fail exactly the same way even without the update.  (It's useful
            # to upload for graph break though, because this can prevent
            # extra graph break compilations.)
            put_code_state()

            return guarded_code
        except Exception as e:
            # NB: e's msg is mutated here to add user stack, but we DON'T want
            # that stack in the Scuba logged fail_reason. So we grab the fail
            # info here and add it to the metrics context below.
            fail_type = type(e).__qualname__
            fail_reason = str(e)
            exception_handler(e, code, frame, export=export)
            # NB: this is the post-mutation exception
            torch._logging.trace_structured(
                "artifact",
                metadata_fn=lambda: {
                    "name": "dynamo_error",
                    "encoding": "string",
                },
                payload_fn=lambda: traceback.format_exc(),
            )
            fail_user_frame_filename, fail_user_frame_lineno = exc.get_exc_message(
                e, compile_id
            )
            if isinstance(
                e,
                (
                    Unsupported,
                    TorchRuntimeError,
                    BackendCompilerFailed,
                    AssertionError,
                    ConstraintViolationError,
                    GuardOnDataDependentSymNode,
                    ValidationException,
                    UncapturedHigherOrderOpError,
                    BisectValidationException,
                    ShortenTraceback,
                ),
            ):
                raise
            else:
                # Rewrap for clarity
                raise InternalTorchDynamoError(
                    f"{type(e).__qualname__}: {str(e)}"
                ).with_traceback(e.__traceback__) from None
        finally:
            # === WARNING WARNING WARNING ===
            # If you commit a bug here, it will suppress writing to
            # dynamo_compile table, and we will not have telemetry.
            # Be extra careful when making changes here!

            if torch._dynamo.config.run_gc_after_compile:
                with dynamo_timed("gc", dynamo_compile_column_us="gc_time_us"):
                    log.info("run_gc_after_compile: running gc")
                    gc.collect(1)

            if tracer:
                tracer.output.local_scope = {}

            from .utils import curr_frame

            frame_key = str(curr_frame)
            if fail_reason is None and output is not None:
                guard_count = len(output.guards)
                shape_env_guard_count = len(output.shape_env.guards)
                graph_op_count = output.count_calls()
                graph_node_count = len(output.graph.nodes)
                graph_input_count = len(output.placeholders)
                non_compliant_ops = {op.__qualname__ for op in output.non_compliant_ops}
                compliant_custom_ops = {
                    op.__qualname__ for op in output.compliant_custom_ops
                }
                torch._dynamo.utils.ReinplaceCounters.log()
            else:
                guard_count = None
                shape_env_guard_count = None
                graph_op_count = None
                graph_node_count = None
                graph_input_count = None
                non_compliant_ops = set({})
                compliant_custom_ops = set({})
                restart_reasons = set()
                # If compilation failed, the entire time is wasted
                dynamo_time_before_restart = (time.time_ns() - start_time_ns) / 1e9

            metrics = {
                "frame_key": frame_key,
                "co_name": code.co_name,
                "co_filename": code.co_filename,
                "co_firstlineno": code.co_firstlineno,
                "cache_size": cache_size.num_cache_entries_with_same_id_matched_objs,
                "accumulated_cache_size": cache_size.num_cache_entries,
                "guard_count": guard_count,
                "shape_env_guard_count": shape_env_guard_count,
                "graph_op_count": graph_op_count,
                "graph_node_count": graph_node_count,
                "graph_input_count": graph_input_count,
                "fail_type": fail_type,
                "fail_reason": fail_reason,
                "fail_user_frame_filename": fail_user_frame_filename,
                "fail_user_frame_lineno": fail_user_frame_lineno,
                "non_compliant_ops": non_compliant_ops,
                "compliant_custom_ops": compliant_custom_ops,
                "restart_reasons": restart_reasons,
                "dynamo_time_before_restart_s": dynamo_time_before_restart,
                "has_guarded_code": guarded_code is not None,
                "config_suppress_errors": config.suppress_errors,
                "config_inline_inbuilt_nn_modules": config.inline_inbuilt_nn_modules,
                "specialize_float": config.specialize_float,
                "is_forward": True,
                "dynamo_compile_time_before_restart_us": to_int_us(
                    dynamo_time_before_restart
                ),
            }
            # TODO: replace with CompileEventLogger.compilation_metrics
            # There are some columns here not in PT2 Compile Events
            # so we need to slightly change it
            metrics_context.update_outer(metrics)
