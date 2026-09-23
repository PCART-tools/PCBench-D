def speculate_subgraph(
    tx,
    f,
    sub_args,
    sub_kwargs,
    description,
    *,
    # source_target is the .value of HigherOrderOpVariable and is the
    # target of the proxy that we created for the higherOrderOperator.
    source_target=None,
    always_restore=False,
    enable_grad=None,
    # NOTE [argument `set_subgraph_inputs`]
    # set_subgraph_inputs controls what how to construct subgraphs' placeholders from sub_args.
    # 1. if your HOP supports arbitrary inputs, use set_subgraph_inputs="automatic" (most recommended).
    # 2. if your HOP supports only Tensor and symnode inputs, use set_subgraph_inputs="flatten_manual" (recommended).
    # If sub_args contain Pytree structure (e.g. dict/list/tuple/set), the sub_args will be flattened first.
    # Then the flattened args are manually set as subgraph's placeholders.
    # 3. if your HOP must preserve inputs that are not tensor or symnode as placeholders e.g. AutogradFunctionContextVariable
    # use set_subgraph_inputs="manual" (not recommended). We do not recommend it in general because it has the
    # restriction that user need to manually control how to create placeholders and VariableTrackers for the args.
    set_subgraph_inputs="automatic",
    restore_side_effects=True,
    should_flatten_outputs=False,
    under_activation_checkpoint=False,
    # Pass in an originating tracer - this is needed for preserving context
    # across fwd-bwd for autograd.Function
    tracer=None,
):
    if sub_kwargs is None:
        sub_kwargs = {}

    assert set_subgraph_inputs in {
        "automatic",
        "semi_automatic",
        "flatten_manual",
        "manual",
    }, "Please use one of the supported set_subgraph_inputs options."

    # See NOTE [Temporary argument `set_subgraph_inputs`]
    if sub_kwargs and set_subgraph_inputs != "automatic":
        unimplemented("Use `set_subgraph_inputs=automatic` when passing `sub_kwargs`.")

    try:
        # ensure guards on args get installed in parent subgraph
        f, sub_args, sub_kwargs = LazyVariableTracker.realize_all(
            (f, sub_args, sub_kwargs),
        )

        with tx.output.subtracer(source_target, tracer) as subtracer:
            sub_args_names = maybe_positional_arg_names(f)
            # User mismatch in the number of args. Will eventually lead to an error.
            if sub_args_names is not None and len(sub_args_names) < len(sub_args):
                sub_args_names = None
            args = validate_args_and_maybe_create_graph_inputs(
                sub_args,
                subtracer,
                tx,
                set_subgraph_inputs,
                description,
                sub_args_names,
            )

            validate_args_and_maybe_create_graph_inputs(
                sub_kwargs.values(),
                subtracer,
                tx,
                set_subgraph_inputs="automatic",
                description=description,
            )

            autograd_ctx = (
                dynamo_enable_grad(tx, enable_grad)
                if enable_grad is not None
                else contextlib.nullcontext()
            )
            checkpoint_ctx = (
                dynamo_under_activation_checkpoint(tx)
                if under_activation_checkpoint
                else contextlib.nullcontext()
            )

            # For handling side effects, we can make an argument that we don't
            # have to do anything here. The side effects infra does a good job
            # of graph breaking if we mutate any nonlocal or global variable
            # while subtracing. As a result if tracing succeeds, side effects
            # data structure will only contain read-only data structures that
            # are put there for tracking purposes.
            # But on the other hand, there is an argument that if we ever write
            # a new side effect in Dynamo which does not go through the side
            # effect infra, we can end up in bad state.
            # Therefore we restore the side effects after tracing. The catch is
            # that we have to special handle tensor variables. If we have seen a
            # nonlocal variable tensor during subtracing, we want to keep a
            # track of that tensor, so that later subtracing or the root tracer
            # itself does not create a new proxy for the already observed tensor
            # variable.
            if restore_side_effects:
                prev_side_effects = tx.output.side_effects.clone()

            with autograd_ctx, checkpoint_ctx:
                output = f.call_function(tx, args, sub_kwargs)

            if restore_side_effects:
                new_side_effects = tx.output.side_effects.clone()
                prev_side_effects.track_tensor_variables_from_runahead_side_effects(
                    new_side_effects
                )
                tx.output.side_effects = prev_side_effects

            treespec = None
            if should_flatten_outputs:
                # Flatten the speculated subgraph output.
                output, treespec = _make_inlined(tx, pytree.tree_flatten)(
                    output
                ).unpack_var_sequence(tx)
                # Actually, transform the list (returned by flatten) into a tuple
                # for dynamo consistency.
                output = BuiltinVariable(tuple).call_function(tx, [output], {})

            # Register output to graph
            # Modeled off of compile_and_call_fx_graph
            # TODO: support pytree output
            # We check always_restore because we dont use the output or side effects of always_restore code,
            # like bwd.
            if always_restore:
                # Nothing left to do here
                return (output, treespec), tx.output.graph, subtracer.lifted_freevars
            else:
                validate_subgraph_output_types(output)

                # The output proxies might not belong to this SubgraphTracer
                # (if they are free variables that were never lifted)
                # so lift them here.
                output_proxies = output.as_proxy()
                output_proxies = pytree.tree_map(
                    subtracer.maybe_lift_tracked_freevar_to_input, output_proxies
                )

                tx.output.create_node(
                    "output",
                    "output",
                    (subtracer.create_arg((output_proxies,))),
                    {},
                )
                graph = tx.output.graph
                graph.lint()
                lifted_freevars = subtracer.lifted_freevars

                # NOTE: [HigherOrderOperator subgraph input ordering]
                # The input ordering of the higher order ops is determined by the order of
                # the creatation of the placehoder.
                # Mannually created inputs are created in validate_args_and_maybe_create_graph_inputs before
                # speculating subgraph.
                # During subgraph speculation, we may lift closured tensors and free symbols as inputs,
                # their ordering is determined by the time they are lifted: earlier lifted ones precede later
                # lifted ones.
                #
                # Suppose the placeholders are
                # O1, O2, X1, O3, O4, X2, X3, O5 where Xs are lifted phs
                # The following code re-order the placeholders to
                # O1, O2, O3, O4, O5, X1, X2, X3
                def move_lifted_freevars_phs_to_end(
                    graph: torch.fx.Graph, lifted_freevars: tuple[torch.fx.Node]
                ):
                    lifted_ph_set = {
                        child_p.node for child_p in lifted_freevars.values()
                    }

                    prev_phs = [n for n in graph.nodes if n.op == "placeholder"]

                    # No need to reorder when graph doesn't have args or doesn't
                    # have lifted freevars or all inputs are lifted freevars.
                    if (
                        len(prev_phs) == 0
                        or len(lifted_ph_set) == 0
                        or len(prev_phs) == len(lifted_ph_set)
                    ):
                        return

                    # Step 1: find first X1
                    for x1 in prev_phs:
                        if x1 in lifted_ph_set:
                            break

                    assert x1 is not None and x1.op == "placeholder"
                    # Step 2: starting from the X1, skip Xs and prepend Os before X1.
                    cand_x = x1.next
                    while cand_x is not None and cand_x.op == "placeholder":
                        if cand_x in lifted_ph_set:
                            cand_x = cand_x.next
                        else:
                            nxt = cand_x.next
                            cand_x._remove_from_list()
                            x1.prepend(cand_x)
                            cand_x = nxt

                    # Step 3: assert that all placeholders are in the correct order as .
                    # in lifted_freevars
                    after_phs = [
                        node for node in graph.nodes if node.op == "placeholder"
                    ][-len(lifted_freevars) :]
                    assert len(after_phs) == len(lifted_freevars)
                    for child_proxy, ph in zip(lifted_freevars.values(), after_phs):
                        assert child_proxy.node is ph, (
                            "The order of placeholders is different from the order of lifted_freevars"
                        )

                    graph.lint()

                if len(lifted_freevars) > 0:
                    move_lifted_freevars_phs_to_end(graph, lifted_freevars)

                return (
                    (output, treespec),
                    graph,
                    lifted_freevars,
                )

    except Unsupported as ex:
        f_name = f"{type(f).__name__}"
        if isinstance(f, UserFunctionVariable):
            f_name = f.get_name()
        msg = (
            f"speculate_subgraph: while introspecting {description}, we were unable "
            f"to trace function `{f_name}` into a single graph. This means "
            f"that Dynamo was unable to prove safety for this API and will "
            f"fall back to eager-mode PyTorch, which could lead to a slowdown."
        )
        log.info(msg)
        log.info(ex)
        raise ex
