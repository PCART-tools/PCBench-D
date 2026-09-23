def make_graphed_callables(callables, sample_args):
    r"""
    Accepts callables (functions or :class:`nn.Module<torch.nn.Module>`\ s)
    and returns graphed versions.

    Each graphed callable's forward pass runs its source callable's
    forward CUDA work as a CUDA graph inside a single autograd node.

    The graphed callable's forward pass also appends
    a backward node to the autograd graph. During backward, this node runs the
    callable's backward work as a CUDA graph.

    Therefore, each graphed callable should be a drop-in replacement for its source callable
    in an autograd-enabled training loop.

    See :ref:`Partial-network capture<partial-network-capture>` for detailed use and constraints.

    If you pass a tuple of several callables, their captures will use the same memory pool.
    See :ref:`Graph memory management<graph-memory-management>` for when this is appropriate.

    Arguments:
        callables (torch.nn.Module or Python function, or tuple of these): Callable or callables to graph.
            See :ref:`Graph memory management<graph-memory-management>` for when passing a tuple of callables
            is appropriate.  If you pass a tuple of callables, their order in the tuple must be the same order
            they'll run in the live workload.
        sample_args (tuple of Tensors, or tuple of tuples of Tensors): Samples args for each callable.
            If a single callable was passed, ``sample_args`` must be a single tuple of argument Tensors.
            If a tuple of callables was passed, ``sample_args`` must be tuple of tuples of argument Tensors.

    .. note::
        The ``requires_grad`` state of each Tensor in ``sample_args`` must match the state
        that's expected for the corresponding real input in the training loop.

    .. warning::
        This API is in beta and may change in future releases.

    .. warning::
        ``sample_args`` for each callable must be a tuple of Tensors. Other types and keyword args
        are not allowed.

    .. warning::
        Returned callables do not support higher order differentiation (e.g., double backward).

    .. warning::
        In any :class:`~torch.nn.Module` passed to :func:`~make_graphed_callables`, only parameters
        may be trainable. Buffers must have ``requires_grad=False``.

    .. warning::
        After you pass a :class:`torch.nn.Module` through :func:`~make_graphed_callables`,
        you may not add or remove any of that Module's parameters or buffers.

    .. warning::
        :class:`torch.nn.Module`\s passed to :func:`~torch.cuda.make_graphed_callables` must not have module hooks
        registered on them at the time they are passed. However, registering hooks on modules *after* passing them
        through :func:`~torch.cuda.make_graphed_callables` is allowed.

    .. warning::
        When running a graphed callable, you must pass its arguments in the same order and format
        they appeared in that callable's ``sample_args``.

    .. warning::
        All Tensor outputs of graphed callables must require grad.
    """
    just_one_callable = False

    if not isinstance(callables, tuple):
        just_one_callable = True
        callables = (callables,)
        sample_args = (sample_args,)

    for c, args in zip(callables, sample_args):
        if isinstance(c, torch.nn.Module):
            assert len(c._backward_hooks) == 0 and len(c._forward_hooks) == 0 and len(c._forward_pre_hooks) == 0, \
                "Modules must not have hooks registered at the time they are passed. However, registering hooks " + \
                "on modules after passing them through make_graphed_callables is allowed."
            assert all(b.requires_grad is False for b in c.buffers()), "In any :class:`~torch.nn.Module` passed to " + \
                ":func:`~make_graphed_callables`, only parameters may be trainable. All buffers must have " + \
                "``requires_grad=False``."
        assert all(isinstance(arg, torch.Tensor) for arg in args), "In the beta API, sample_args " + \
            "for each callable must be a tuple of Tensors. Other types and keyword args are not allowed."


    # If a callable is an nn.Module, its graph's full input surface is the args the user explicitly
    # passes to forward (ie, its sample_args) AND the module's parameter attributes.
    per_callable_len_user_args = [len(args) for args in sample_args]
    per_callable_module_params = [tuple(c.parameters()) if isinstance(c, torch.nn.Module) else ()
                                  for c in callables]
    per_callable_static_input_surfaces = [sample_args[i] + per_callable_module_params[i]
                                          for i in range(len(callables))]

    fwd_graphs = [torch.cuda.CUDAGraph() for _ in range(len(callables))]
    bwd_graphs = [torch.cuda.CUDAGraph() for _ in range(len(callables))]

    mempool = graph_pool_handle()

    # Warmup
    # Hopefully prevents cudnn benchmarking and other lazy-initialization cuda work
    # from ending up in any captures.
    torch.cuda.synchronize()
    with torch.cuda.stream(torch.cuda.Stream()):
        for func, args, static_input_surface in zip(callables,
                                                    sample_args,
                                                    per_callable_static_input_surfaces):
            for _ in range(3):
                outputs = func(*args)
                outputs = (outputs,) if isinstance(outputs, torch.Tensor) else outputs
                grad_inputs = torch.autograd.grad(outputs=outputs,
                                                  inputs=tuple(i for i in static_input_surface if i.requires_grad),
                                                  grad_outputs=tuple(torch.empty_like(o) for o in outputs),
                                                  only_inputs=True,
                                                  allow_unused=False)
            del outputs, grad_inputs
    torch.cuda.synchronize()

    # All captures here share a mempool. To avoid replays corrupting each other's memory,
    # the safest approach is to capture all passes in the same order they'll run:
    # fwd 1, fwd 2, ... fwd N, then bwd N, bwd N-1, ... bwd 1.

    # Capture forward graphs
    per_callable_static_outputs = []
    per_callable_output_was_tensor = []
    for func, args, fwd_graph in zip(callables,
                                     sample_args,
                                     fwd_graphs):
        with torch.cuda.graph(fwd_graph, pool=mempool):
            outputs = func(*args)

        # Assumes model output is a tensor or tuple of tensors
        if isinstance(outputs, torch.Tensor):
            per_callable_output_was_tensor.append(True)
            outputs = (outputs,)
        else:
            per_callable_output_was_tensor.append(False)

        per_callable_static_outputs.append(outputs)

    # Capture backward graphs in reverse order
    per_callable_static_grad_outputs = []
    per_callable_static_grad_inputs = []
    for static_input_surface, static_outputs, bwd_graph, module_params in \
            zip(reversed(per_callable_static_input_surfaces),
                reversed(per_callable_static_outputs),
                reversed(bwd_graphs),
                reversed(per_callable_module_params)):

        # For now, assumes all static_outputs require grad
        assert all(o.requires_grad for o in static_outputs), "Outputs of graphed callables must require grad."
        static_grad_outputs = tuple(torch.empty_like(o) for o in static_outputs)

        with torch.cuda.graph(bwd_graph, pool=mempool):
            grad_inputs = torch.autograd.grad(outputs=static_outputs,
                                              inputs=tuple(i for i in static_input_surface if i.requires_grad),
                                              grad_outputs=static_grad_outputs,
                                              only_inputs=True,
                                              allow_unused=False)

        # Constructs a tuple suitable for returning from Graphed.backward:
        # Pads out the actually-needed grads with Nones in gradient slots for inputs that don't require grad.
        # I couldn't think of a slick one-liner for this pattern.
        static_grad_inputs = []
        grad_idx = 0
        for arg in static_input_surface:
            if arg.requires_grad:
                static_grad_inputs.append(grad_inputs[grad_idx])
                grad_idx += 1
            else:
                static_grad_inputs.append(None)  # type: ignore[arg-type]
        static_grad_inputs = tuple(static_grad_inputs)  # type: ignore[assignment]

        per_callable_static_grad_outputs.append(static_grad_outputs)
        per_callable_static_grad_inputs.append(static_grad_inputs)

    # Reverses the most recent two lists
    per_callable_static_grad_outputs = list(reversed(per_callable_static_grad_outputs))
    per_callable_static_grad_inputs = list(reversed(per_callable_static_grad_inputs))
    # Now for every per_callable list, per_callable_*[i] holds the stuff for the ith callable.

    def make_graphed_autograd_function(fwd_graph,
                                       bwd_graph,
                                       module_params,
                                       len_user_args,
                                       output_was_tensor,
                                       static_input_surface,
                                       static_outputs,
                                       static_grad_outputs,
                                       static_grad_inputs):
        class Graphed(torch.autograd.Function):
            @staticmethod
            def forward(ctx, *inputs):
                # At this stage, only the user args may (potentially) be new tensors.
                for i in range(len_user_args):
                    if static_input_surface[i].data_ptr() != inputs[i].data_ptr():
                        static_input_surface[i].copy_(inputs[i])
                fwd_graph.replay()
                assert isinstance(static_outputs, tuple)
                return tuple(o.detach() for o in static_outputs)

            @staticmethod
            @torch.autograd.function.once_differentiable
            def backward(ctx, *grads):
                for g, grad in zip(static_grad_outputs, grads):
                    if g is None:
                        assert grad is None
                    else:
                        # don't copy if autograd gods have been kind and the
                        # incoming grad is already in the right place
                        if g.data_ptr() != grad.data_ptr():
                            g.copy_(grad)
                bwd_graph.replay()

                # Input args that didn't require grad expect a None gradient.
                assert isinstance(static_grad_inputs, tuple)
                return tuple(b.detach() if b is not None else b for b in static_grad_inputs)

        def functionalized(*user_args):
            # Runs the autograd function with inputs == all inputs to the graph that might require grad
            # (explicit user args + module parameters)
            # Assumes module params didn't change since capture.
            out = Graphed.apply(*(user_args + module_params))
            return out[0] if output_was_tensor else out

        return functionalized

    # Put together the final graphed callables
    ret = []
    for i, func in enumerate(callables):
        graphed = make_graphed_autograd_function(fwd_graphs[i],
                                                 bwd_graphs[i],
                                                 per_callable_module_params[i],
                                                 per_callable_len_user_args[i],
                                                 per_callable_output_was_tensor[i],
                                                 per_callable_static_input_surfaces[i],
                                                 per_callable_static_outputs[i],
                                                 per_callable_static_grad_outputs[i],
                                                 per_callable_static_grad_inputs[i])

        if isinstance(func, torch.nn.Module):
            def make_graphed_forward(func, graph_training_state, graphed, orig_fwd):
                def new_fwd(*user_args):
                    # If the module's training-or-eval state matches what we graphed,
                    # run the graph, otherwise run the original forward method
                    if func.training == graph_training_state:
                        return graphed(*user_args)
                    else:
                        return orig_fwd(*user_args)
                return new_fwd
            func.forward = make_graphed_forward(func, func.training, graphed, func.forward)  # type: ignore[assignment]
            ret.append(func)
        else:
            ret.append(graphed)

    if just_one_callable:
        return ret[0]

    return tuple(ret)
