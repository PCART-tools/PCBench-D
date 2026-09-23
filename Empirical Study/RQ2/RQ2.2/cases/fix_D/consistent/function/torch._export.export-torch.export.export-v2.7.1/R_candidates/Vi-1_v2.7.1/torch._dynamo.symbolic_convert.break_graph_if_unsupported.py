def break_graph_if_unsupported(*, push):
    def decorator(inner_fn):
        @functools.wraps(inner_fn)
        def wrapper(self: "InstructionTranslatorBase", inst: Instruction):
            speculation = self.speculate()
            if speculation.failed:
                assert speculation.reason is not None
                return handle_graph_break(self, inst, speculation.reason)
            try:
                return inner_fn(self, inst)
            except Unsupported as excp:
                if self.active_generic_context_managers:
                    # We don't support graph break under GenericContextWrappingVariable,
                    # If there is, we roll back to the checkpoint and fall back.
                    excp.remove_from_stats()
                    unimplemented_v2(
                        gb_type="Graph break under GenericContextWrappingVariable",
                        context=f"Active generic context managers: {self.active_generic_context_managers}",
                        explanation="Attempted to graph break in an active context manager(s) that doesn't support graph breaking.",
                        hints=[
                            "Move the offending context manager(s) to outside the compiled region.",
                            *graph_break_hints.CAUSED_BY_EARLIER_GRAPH_BREAK,
                        ],
                        from_exc=excp,
                    )

                if isinstance(excp, exc.UncapturedHigherOrderOpError):
                    raise

                if not self.should_compile_partial_graph():
                    raise

                log_graph_break(
                    self.code_options,
                    exc_info=True,
                    reason=str(excp),
                    user_stack=excp.real_stack,
                )

                if self.maybe_has_backedge():
                    msg = (
                        "Skipping frame because there is a graph break in a for/while loop\n"
                        f"{self.frame_summary()}"
                    )
                    log.info(msg)
                    raise exc.SkipFrame(msg) from excp

                excp.remove_from_stats()
                excp.add_to_stats("graph_break")
                speculation.reason = GraphCompileReason(excp.msg, excp.real_stack)
            speculation.fail_and_restart_analysis()

        def handle_graph_break(
            self: "InstructionTranslatorBase",
            inst: Instruction,
            reason: GraphCompileReason,
        ):
            self.output.compile_subgraph(self, reason=reason)
            cg = PyCodegen(self)
            cleanup: list[Instruction] = []
            # Reconstruct the context variable CLASS in the block stack
            for b in self.block_stack:
                # Don't exit any modes we have entered,
                # output bytecode will mutate the tf mode stack accordingly
                if isinstance(b.with_context, TorchFunctionModeVariable):
                    cg.extend_output(
                        b.resume_fn().try_except_torch_function_mode(
                            cg.code_options, cleanup
                        )
                    )
                    continue
                assert b.with_context is not None
                assert isinstance(b.with_context, (ContextWrappingVariable))
                b.with_context.reconstruct_type(cg)
                cg.extend_output(b.resume_fn().try_finally(cg.code_options, cleanup))
            self.output.add_output_instructions(cg.get_instructions())
            del cg

            if sys.version_info >= (3, 11) and inst.opname == "CALL":
                kw_names = (
                    self.kw_names.as_python_constant()
                    if self.kw_names is not None
                    else ()
                )
                if len(kw_names) > 0:
                    # KW_NAMES no longer used in 3.13
                    assert sys.version_info < (3, 13)
                    self.output.add_output_instructions(
                        [create_instruction("KW_NAMES", argval=kw_names)]
                    )
                call_insts = create_call_function(inst.arg, False)
                call_insts[-1].copy_positions(inst)
                self.output.add_output_instructions(call_insts)
            else:
                # copy instruction, but without exception table data
                assert inst.target is None
                inst_copy = copy.copy(inst)
                inst_copy.exn_tab_entry = None
                self.output.add_output_instructions([inst_copy])

            self.output.add_output_instructions(cleanup)

            if (
                sys.version_info >= (3, 11)
                and sys.version_info < (3, 12)
                and inst.opname == "CALL"
            ):
                # stack effect for PRECALL + CALL is split between the two instructions
                stack_effect = dis.stack_effect(
                    dis.opmap["PRECALL"], inst.arg
                ) + dis.stack_effect(dis.opmap["CALL"], inst.arg)
            else:
                stack_effect = dis.stack_effect(inst.opcode, inst.arg)
            self.popn(push - stack_effect)

            for _ in range(push):
                self.push(UnknownVariable())
            self.output.add_output_instructions(
                self.create_call_resume_at(self.next_instruction)
            )

        return wrapper

    return decorator
