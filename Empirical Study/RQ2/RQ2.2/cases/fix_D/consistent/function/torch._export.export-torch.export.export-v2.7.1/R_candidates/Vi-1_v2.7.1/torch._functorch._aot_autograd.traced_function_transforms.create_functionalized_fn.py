def create_functionalized_fn(
    fn,
    args,
    *,
    meta: ViewAndMutationMeta,
    aot_config: AOTConfig,
    trace_joint: bool,
) -> Any:
    @wraps(fn)
    def _functionalized_f_helper(*args):
        with maybe_enable_thunkify():
            # See Note [Disabling Functionalize TLS Above Python Functionalization]
            disable_above = torch._C._ExcludeDispatchKeyGuard(
                torch._C.DispatchKeySet(torch._C.DispatchKey.Functionalize)
            )

            with disable_above:
                # The functionalization code here can potentially trigger traces
                # into the graph, but we'd prefer to NOT do this, because if we
                # trace them now, we will end up with FX nodes that don't have
                # module stack annotations, which makes unflattener unhappy.
                # Wrap inputs into functional wrappers
                f_args = pytree.tree_map(to_fun, args)

                # Run the joint
                f_outs = fn(*f_args)

            if trace_joint:
                # We support a limited amount of mutation of graph inputs during the backward pass.
                # (This is used e.g. by Float8, which needs to update buffers during the backward pass)
                # Here, we perform extra checks for primals that were mutated in the **backward**
                # We're doing the checks here instead of doing them with the rest of the input mutation handling because:
                # - We need to detect inputs that were mutated in the backward **separately** from mutations that happened
                #   during the forward, because the handling is different: some input mutations from the the forward
                #   can be only handled in a fw-only runtime epilogue, and in theory if we wanted to handle those same
                #   types of mutations in the backward we would need a bw-only runtime epilogue.
                # - We could in theory have our analysis pass differentiate mutations in the fw from mutations in
                #   the bw by running our analysis first on the fw-only graph, and then on the joint graph. This would
                #   require an extra round of tracing though, so it's more efficient to do in-line here.
                assert (
                    isinstance(args, tuple)
                    and len(args) == 2
                    and isinstance(args[0], (list, tuple))
                )
                # Only look at mutations that happened to forward inputs (e.g. fw buffers that were saved for bw)
                primals_before = args[0]
                primals_after = pytree.tree_map(from_fun, f_args[0])
                for idx, (f_inpt, before, after, inpt_info) in enumerate(
                    zip(f_args[0], primals_before, primals_after, meta.input_info)
                ):
                    # Store information about mutations in joint(for backward analysis)
                    joint_mutates_data = has_data_mutation(f_inpt)

                    joint_mutates_metadata = has_metadata_mutation(
                        f_inpt, before, check_only_storage_mutation=False
                    )

                    # Ban metadata mutations on fw inputs during the bw
                    if not inpt_info.mutates_metadata:
                        assert (
                            not joint_mutates_metadata
                        ), "Found a graph input that had its metadata mutated in the backward. This is not supported"

                    # Ban storage resizing on fw inputs during the bw
                    if not inpt_info.mutation_inductor_storage_resize:
                        assert not was_inductor_storage_resized(
                            f_inpt
                        ), "Found a graph input that had storage resizing in the backward. This is not supported"

                    # Allow data mutations on fw inputs during the bw, but only if they do not require grad
                    # So we can guarantee that we can keep the mutations in the graph
                    if (
                        joint_mutates_data
                        and not inpt_info.mutates_data
                        and not inpt_info.mutates_storage_metadata
                    ):
                        # Not banning here mutations on inpt_info.requires_grad -
                        # we'll check at runtime and fail only when backward is under torch.is_grad_enabled (create_graph)
                        # Add node meta for copy_ for partitioner that this node should be in backward graph.
                        with torch.fx.traceback.preserve_node_meta(), set_partitioner_tag_must_be_in_backward():
                            before.copy_(after)
                        meta.indices_of_inputs_that_requires_grad_with_mutations_in_bw.append(
                            idx
                        )
                # Now that we covered mutations to *forward* inputs during the backward,
                # we also need to cover mutations to *backward-only* inputs during the backward (e.g. mutation to a grad_out).
                # Today, we will just error in all cases of this happening unless someone needs us to support it.
                tangents_before = args[1]
                tangents_after = pytree.tree_map(from_fun, f_args[1])
                for f_inpt, before, after in zip(
                    f_args[1], tangents_before, tangents_after
                ):
                    assert not has_metadata_mutation(
                        f_inpt, before, check_only_storage_mutation=False
                    ), "Found an input to the backward that had metadata mutated during the backward pass. This is not supported"
                    if has_data_mutation(f_inpt):
                        can_be_in_graph = _check_if_mutation_can_be_in_graph(
                            keep_input_mutations=True,
                            mutates_data=True,
                            mutates_metadata=False,
                            mutations_hidden_from_autograd=are_all_mutations_hidden_from_autograd(
                                f_inpt
                            ),
                            mutations_under_no_grad_or_inference_mode=are_all_mutations_under_no_grad_or_inference_mode(
                                f_inpt
                            ),
                            mutates_storage_metadata=False,
                            mutation_inductor_storage_resize=was_inductor_storage_resized(
                                f_inpt
                            ),
                            requires_grad=f_inpt.requires_grad,
                        )
                        assert (
                            can_be_in_graph
                        ), "a backward input that had data mutated in an autograd-aware way. This is not supported"
                        # Perform the input mutation
                        with torch.fx.traceback.preserve_node_meta():
                            before.copy_(after)

            if aot_config.keep_inference_input_mutations:
                # Note: This is a bit annoying. There's a layering issue here, where:
                # (1) functionalization needs to operate on **synthetic base** inputs, before unpacking them into the "real" inputs.
                # (2) For keep_input_mutations, we support tracing a call to copy_() directly on mutated inputs.
                #     However, we **only** want to support this for inputs that have data-only (and no metadata) mutations,
                #     because inductor (and backends in generally) would prefer not to see these (e.g. as_strided_(), resize_()).
                #     This makes it pretty difficult for this logic to operate on synthetic bases.
                # (3) In addition, there are cases where it's significantly cheaper to perform the copy on the individual
                #     (unpacked) input aliases, instead of the synthetic base.
                # Example case where (3) could be important:
                #
                #     def f(x, y):
                #         x.mul_(2)
                #         y.mul_(3)
                #         return x, y
                #    a = torch.ones(1'000'000)
                #    x, y = out(a[0:9], a[1:10])
                #
                # It would be much better to add copy_() calls into the graph for the two tiny slices, instead of materializing
                # a giant "updated synthetic base" and copying into a's entire storage.
                #
                # For now, we are pessimistically not performing the optimization from (3);
                # we will materialize an "updated" synthetic base, and copy it back to the synthetic input base.
                # This allows us to factor aot autograd much more nicely, since only one area of the code needs to worry
                # about synthetic bases.
                for i, (inpt_old, inpt_f) in enumerate(
                    zip(args, f_args) if not trace_joint else zip(args[0], f_args[0])
                ):
                    if not isinstance(inpt_f, torch.Tensor):
                        continue
                    assert is_fun(inpt_f)
                    inpt_new = from_fun(inpt_f)
                    if (
                        meta.input_info[i].mutation_type
                        == MutationType.MUTATED_IN_GRAPH
                    ):
                        # See Note [set_() Input Mutations in AOTAutograd]
                        # all mutations on the input must be under no_grad, so it is safe to put in the graph
                        # Here, we're saying that if an input experienced a set call, inp.set_(other),
                        # then we can effectively not have to worry about whether its data was mutated.
                        # There are 3 cases:
                        # (1) We mutate inp *after* the set_() call. other is a graph intermediate.
                        #     In this case, we're not really mutating the input storage of "inp";
                        #     we're mutating the storage of an intermdiate value (other),
                        #     and slamming that storage into the input tensor. So no data mutation is necessary.
                        # (2) We mutate inp *after* the set_() call. other is a graph *input*.
                        #     In this case, the data mutation will be properly handled in the runtime
                        #     epilogue during the processing of "other"
                        # (3) We mutate inp *before* the set_() call.
                        #     This case is *not* currently handled.
                        if meta.input_info[i].mutates_storage_metadata:
                            with torch.no_grad():
                                inpt_old.set_(inpt_new)

                        # Note [Ordering of resize_() and set_()]
                        # Importantly: the common usage in FSDP is that we have a dummy parameter
                        # that sees a set_() and **Then** a resize_().
                        # We must put those mutations into the graph in the same order,
                        # Since running them in the opposite order will have different behavior.
                        # We fully ban resize_() followed by set_() for now, although in principal
                        # we could support this
                        if meta.input_info[i].mutation_inductor_storage_resize:
                            # resizing is not supported on subclasses (we error earlier if this happens)
                            from torch._subclasses.functional_tensor import (
                                FunctionalTensor,
                            )

                            assert isinstance(inpt_f, FunctionalTensor)
                            old_storage_size = torch._functionalize_get_storage_size(  # type: ignore[attr-defined]
                                inpt_f.elem, before=True
                            )
                            new_storage_size = torch._functionalize_get_storage_size(  # type: ignore[attr-defined]
                                inpt_f.elem, before=False
                            )
                            if old_storage_size != new_storage_size:
                                assert (
                                    old_storage_size == 0 or new_storage_size == 0
                                ), f"""\
    Encountered a storage resize during tracing on input {i}. Old nbytes={old_storage_size}, new nbytes={new_storage_size}
    We only support storage resizing on graph inputs as long as the input either starts or ends with a storage size of 0
    (the case for FSDP)"""
                                torch.ops.inductor.resize_storage_bytes_(
                                    inpt_old, new_storage_size
                                )
                            if new_storage_size == 0:
                                # Even if we marked the input as having a data mutation (thus needing a copy_()),
                                # We should **ignore** it if our input has no storage
                                # (this can happen if, e.g. we temporarily resize our input, copy data into it,
                                #  and resize it back down to zero)
                                continue
                        # Optimization: if the copy_() is a no-op then don't include it in the graph.
                        # In theory inductor could optimize this away, however in fsdp, we end up with
                        # param.copy_(param), where param is a zero-storage-size tensor,
                        # and running this op in eager mode (using the aot_eager backend) will result in a segfault.
                        # So we may as well optimize it away here.
                        if inpt_old is inpt_new:
                            # (This check needs to be done after putting resize_() in the graph,
                            # since a resize_(0) doesn't actually change the FunctionalTensor's inner tensor)
                            continue
                        # We found an input that had a (data-only) mutation.
                        # Since keep_input_mutations is set, we need to faithfully apply a copy_()
                        # so the compiler will see the input mutation in the graph.
                        if (
                            meta.input_info[i].mutates_data
                            and meta.input_info[i].mutations_hidden_from_autograd
                        ):
                            # Hidden from autograd = run under no_grad, **and** don't bump VC
                            # (although if the tensor was created in inference mode, it has no VC)
                            if inpt_old.is_inference():
                                maybe_preserve_vc = nullcontext()
                            else:
                                maybe_preserve_vc = torch.autograd._unsafe_preserve_version_counter(
                                    inpt_old  # type: ignore[assignment]
                                )
                            with torch.no_grad(), maybe_preserve_vc:
                                inpt_old.copy_(inpt_new)
                        elif (
                            meta.input_info[i].mutates_data
                            and meta.input_info[
                                i
                            ].mutations_under_no_grad_or_inference_mode
                        ):
                            # Under no_grad = run under no_grad (we still bump the VC though)
                            # (inference_mode will also bump the VC, as long as the tensor in question
                            # was created outside of inference_mode)
                            with torch.no_grad():
                                inpt_old.copy_(inpt_new)
                        elif meta.input_info[i].mutates_data:
                            inpt_old.copy_(inpt_new)

                # When an output tensor is a functionalized mutated input, and we
                # were able to move the mutation in to the graph then we can return
                # the mutated input directly. This prevents duplicating the
                # tensors contents.
                flat_outs, outs_spec = pytree.tree_flatten(f_outs)
                flat_outs = [from_fun(o) for o in flat_outs]
                num_outs = len(meta.output_info)

                for i in range(num_outs):
                    info = meta.output_info[i]
                    if info.output_type != OutputType.is_input:
                        continue

                    assert info.base_idx is not None
                    if (
                        meta.input_info[info.base_idx].mutation_type
                        == MutationType.MUTATED_IN_GRAPH
                    ):
                        fw_args = args[0] if trace_joint else args
                        flat_outs[i] = fw_args[info.base_idx]
                return pytree.tree_unflatten(flat_outs, outs_spec)

            return pytree.tree_map(from_fun, f_outs)

    # Kinda annoying, but needed to make sure that the fx graph we trace out has "primals"
    # and "tangents" as its input names (which are special-cased by the partitioner)
    # TODO (tmanlaibaatar) revisit this if we ever need to turn on non-strict joint graph export
    def joint_helper(primals, tangents):
        return _functionalized_f_helper(primals, tangents)

    helper = joint_helper if trace_joint else _functionalized_f_helper
    if config.functionalize_rng_ops:
        # Setup the wrapper for functionalization of rng ops
        helper, args = create_functionalized_rng_ops_wrapper(helper, args, trace_joint)

    return helper, args
