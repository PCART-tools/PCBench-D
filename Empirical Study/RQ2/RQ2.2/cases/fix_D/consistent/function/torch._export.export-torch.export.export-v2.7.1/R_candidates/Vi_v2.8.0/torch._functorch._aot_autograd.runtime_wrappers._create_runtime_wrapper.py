def _create_runtime_wrapper(
    compiled_fn,
    *,
    runtime_metadata: ViewAndMutationMeta,
    indices_of_inps_to_detach: list[int],
    trace_joint: bool,
    keep_input_mutations: bool,
    disable_amp: bool,
):
    if not getattr(compiled_fn, "_boxed_call", False):
        compiled_fn = make_boxed_func(compiled_fn)

    # Note [Inputs needed in runtime epilogue after list clearing]
    # In Python functions, you can't free the input arguments of a function within the scope of that function. A workaround is to
    # wrap the input arguments in a list, and clear the list from within the function.
    # Here, this is implemented as `call_func_at_runtime_with_args(..., steal_args=True)`.
    #
    # This is needed for Compiled Autograd since some of the inputs (activations) should be freed early.
    # However, we cannot blindly clear the entire list, because AOTAutograd may need access to some of the graph inputs
    # **after** the compiled function has finished running. There are two main cases:
    #   (1) Input mutations: If there are an input mutations that we must run outside of the graph, we need access to the input.
    #   (2) Output aliasing: Outputs that aliases graph inputs generally must be regenerated outside of the `autograd.Function`,
    #       and doing so requires us accessing the corresponding input after the compiled artifact has run.
    epilogue_args_idx = []
    epilogue_args_idx.extend(runtime_metadata.mutated_inp_runtime_indices)
    for info in runtime_metadata.output_info:
        if (
            info.output_type == OutputType.alias_of_input
            or info.output_type == OutputType.is_input
        ):
            assert isinstance(info.base_idx, int)
            epilogue_args_idx.append(info.base_idx)

    if config.unlift_effect_tokens:
        assert len(runtime_metadata.tokens) == 0

    if runtime_metadata.num_outputs_aliased > 0:
        output_handlers = tuple(
            make_output_handler(info, runtime_metadata, trace_joint)
            for info in runtime_metadata.output_info
        )

    def record_runtime_wrapper_prologue_enter() -> (
        Optional[AbstractContextManager[None]]
    ):
        if (
            torch.autograd.profiler._is_profiler_enabled
            and dynamo_config.record_runtime_overhead
        ):
            cm = torch._C._profiler._RecordFunctionFast(
                "AOTDispatcher Runtime Wrapper Prologue"
            )
            cm.__enter__()
            return cm
        return None

    def record_runtime_wrapper_prologue_exit(
        cm: Optional[AbstractContextManager[None]],
    ) -> None:
        if cm is not None:
            cm.__exit__(None, None, None)

    def runtime_wrapper(args: list[Any]):
        # Create context manager for profiler
        cm = record_runtime_wrapper_prologue_enter()

        # stash a ref to each input tensor we plan to use after the compiled function
        orig_inputs = {i: args[i] for i in epilogue_args_idx}

        if keep_input_mutations:
            mutated_args = (
                args[i]
                for i in runtime_metadata.mutated_graph_handled_indices_seen_by_autograd
            )
            torch.autograd.graph.increment_version(mutated_args)

        if trace_joint:
            args_ = list(args)
            # See Note [Detaching inputs that never need gradients]
            for idx in indices_of_inps_to_detach:
                if isinstance(args_[idx], torch.Tensor):
                    args_[idx] = args_[idx].detach()

            # It's possible to have trace_joint inside user specified with no_grad() region,
            # if there is a nested with enable_grad(), that forces some outputs to require gradients.
            # Therefore, we unconditionally turn on enable_grad() for compiled_fn execution.
            with (
                torch.autograd._force_original_view_tracking(True),
                torch.enable_grad(),
            ):
                record_runtime_wrapper_prologue_exit(cm)
                all_outs = call_func_at_runtime_with_args(
                    compiled_fn, args_, disable_amp=disable_amp, steal_args=True
                )
        else:
            # When we have an inference graph, we run with grad disabled.
            # It's possible to get an inference graph with inputs that require grad,
            # in which case we want to make sure autograd is disabled
            # (since e.g., inductor will generate aten.addmm.out calls which autograd will complain on)
            # NOTE: We use _set_grad_enabled directly to reduce runtime overhead
            grad_enabled = torch.is_grad_enabled()
            try:
                if grad_enabled:
                    torch._C._set_grad_enabled(False)
                record_runtime_wrapper_prologue_exit(cm)
                all_outs = call_func_at_runtime_with_args(
                    compiled_fn, args, disable_amp=disable_amp, steal_args=True
                )
            finally:
                if grad_enabled:
                    torch._C._set_grad_enabled(True)
        del args

        num_mutated_runtime_inps = runtime_metadata.num_mutated_inp_runtime_indices
        num_intermediate_bases = runtime_metadata.num_intermediate_bases

        assert (
            len(all_outs)
            == num_mutated_runtime_inps
            + runtime_metadata.num_outputs
            + num_intermediate_bases
        )

        # Step 3: After running the compiled fw, apply updates to mutated inputs
        num_mutations_to_apply = runtime_metadata.num_mutated_inp_runtime_indices
        if num_mutations_to_apply > 0:
            updated_inputs = all_outs[:num_mutations_to_apply]
            fw_outs = all_outs[num_mutations_to_apply:]

            for i, inpt_idx in enumerate(runtime_metadata.mutated_inp_runtime_indices):
                meta = runtime_metadata.input_info[inpt_idx]
                if not meta.mutates_data and not meta.mutates_metadata:
                    continue
                original_inpt = orig_inputs[inpt_idx]
                updated_inpt = updated_inputs[i]
                if meta.mutates_storage_metadata:
                    # See Note [set_() Input Mutations in AOTAutograd]
                    # mutates_storage_metadata means our input saw a x.set_(y) call.
                    # What if x **also** saw a data and/or a metadata mutation?
                    # (1) If the [meta]data mutation occurred after the set_(),
                    #     then there is no need to copy_() the data.
                    #     When we perform x.set_(x_updated), we are guaranteed that
                    #     x_updated already has the final version of the data/metadata
                    # (2) If a data mutation occurred before the set_().
                    #     This case seems very difficult to support.
                    #     TODO: discuss on the PR and decide if we want to tr to
                    #     either support it, or detect and ban it.
                    if trace_joint:
                        assert isinstance(updated_inpt, TensorAlias)
                        updated_inpt = updated_inpt.alias
                    with torch.no_grad():
                        original_inpt.set_(updated_inpt)
                    continue
                if meta.mutates_metadata and not meta.mutates_data:
                    if trace_joint:
                        assert isinstance(updated_inpt, TensorAlias)
                        updated_inpt = updated_inpt.alias
                    # We need to grab the size/stride/storage_offset from the compiled forward,
                    # and use that to mutate the metadata of the input
                    original_inpt.as_strided_(
                        updated_inpt.size(),
                        updated_inpt.stride(),
                        updated_inpt.storage_offset(),
                    )
                else:
                    if meta.mutates_data and meta.mutates_metadata:
                        original_inpt.as_strided_(
                            updated_inpt.size(),
                            updated_inpt.stride(),
                            updated_inpt.storage_offset(),
                        )
                    else:
                        assert meta.mutates_data
                    if meta.is_leaf and original_inpt.requires_grad:
                        # We can hit this situation in this case:
                        #   def f(x):
                        #       x.detach().mul_(2)
                        #       return x + 1
                        # AOTAutograd will see a mutation in the above case, and try to
                        # apply a copy_() here, in the epilogue.
                        # But if x required gradients, and is a leaf, then autograd
                        # will yell at us for trying to mutate it.
                        # However, it's only possible to end up in this scenario (like the above)
                        # if all of the mutations to the leaf input were non-autograd-tracking mutations
                        # (aka mutations under no_grad(), or on detached views).
                        # In that case, we fully want to hide the mutation from autograd, so detaching is ok.
                        original_inpt.detach().copy_(updated_inpt)
                    else:
                        original_inpt.copy_(updated_inpt)
        else:
            fw_outs = all_outs

        # Step 4: Manually regenerate any outputs that are aliased to inputs, instead of
        # compiling them.
        if runtime_metadata.num_outputs_aliased > 0:
            # The compiled forward also returned intermediate bases. We don't want to return them to the user.
            expect_num_outputs = (
                len(output_handlers) + runtime_metadata.num_intermediate_bases
            )
            assert len(fw_outs) == expect_num_outputs
            ret_outs = [
                handler(orig_inputs, fw_outs, out)
                for out, handler in builtins.zip(fw_outs, output_handlers)
            ]
        else:
            ret_outs = fw_outs

        if runtime_metadata.dynamic_outputs:
            for t, o in zip(ret_outs, runtime_metadata.output_info):
                if o.dynamic_dims is None:
                    continue
                maybe_mark_dynamic_helper(t, o.dynamic_dims)
        if runtime_metadata.grad_enabled_mutation is not None:
            torch._C._set_grad_enabled(runtime_metadata.grad_enabled_mutation)
        return ret_outs

    if not (trace_joint and _should_disable_saved_tensors_hooks()):
        return runtime_wrapper

    # Disabling saved tensors hooks
    def _runtime_wrapper(*args, **kwargs):
        with _disable_saved_tensors_hooks():
            return runtime_wrapper(*args, **kwargs)

    return _runtime_wrapper
