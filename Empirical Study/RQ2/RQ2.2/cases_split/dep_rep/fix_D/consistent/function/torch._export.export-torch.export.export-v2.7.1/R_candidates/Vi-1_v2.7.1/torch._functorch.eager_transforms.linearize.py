@exposed_in("torch.func")
def linearize(func: Callable, *primals) -> tuple[Any, Callable]:
    """
    Returns the value of ``func`` at ``primals`` and linear approximation
    at ``primals``.

    Args:
        func (Callable): A Python function that takes one or more arguments.
        primals (Tensors): Positional arguments to ``func`` that must all be
            Tensors. These are the values at which the function is linearly approximated.

    Returns:
        Returns a ``(output, jvp_fn)`` tuple containing the output of ``func``
        applied to ``primals`` and a function that computes the jvp of
        ``func`` evaluated at ``primals``.

    linearize is useful if jvp is to be computed multiple times at ``primals``. However,
    to achieve this, linearize saves intermediate computation and has higher memory requirements
    than directly applying `jvp`. So, if all the ``tangents`` are known, it maybe more efficient
    to compute vmap(jvp) instead of using linearize.

    .. note::
        linearize evaluates ``func`` twice. Please file an issue for an implementation
        with a single evaluation.

    Example::
        >>> import torch
        >>> from torch.func import linearize
        >>> def fn(x):
        ...     return x.sin()
        ...
        >>> output, jvp_fn = linearize(fn, torch.zeros(3, 3))
        >>> jvp_fn(torch.ones(3, 3))
        tensor([[1., 1., 1.],
                [1., 1., 1.],
                [1., 1., 1.]])
        >>>

    """
    # Note: We evaluate `fn` twice.
    # Once for returning the output and other while
    # tracing the graph.
    # If this becomes a bottle-neck, we should update
    # make_fx such that it also returns the output.

    output = func(*primals)
    _, output_spec = tree_flatten(output)

    flat_primals, primals_argspec = tree_flatten(primals)

    # tangents for tracing
    flat_tangents = tuple(p.new_empty(()).expand_as(p) for p in flat_primals)

    # function to trace
    def trace_fn(flat_tangents):
        with fwAD.dual_level():
            flat_duals = tuple(
                fwAD.make_dual(p, t) for p, t in zip(flat_primals, flat_tangents)
            )
            duals = tree_unflatten(flat_duals, primals_argspec)
            output = func(*duals)
            tangents = tree_map_only(
                torch.Tensor, lambda dual: safe_unpack_dual(dual, False)[1], output
            )

        return tangents

    jvp_graph = lazy_dynamo_disallow(make_fx)(trace_fn)(flat_tangents)
    const_folded_jvp_graph = lazy_dynamo_disallow(const_fold.split_const_subgraphs)(
        jvp_graph
    )

    # Hold only the meta-data regarding the primals.
    flat_primals_shape = tuple(p.shape for p in flat_primals)
    flat_primals_device = tuple(p.device for p in flat_primals)
    flat_primals_dtype = tuple(p.dtype for p in flat_primals)

    def forward_ad_checks(flat_tangents):
        for idx, t in enumerate(flat_tangents):
            if t.shape != flat_primals_shape[idx]:
                msg = (
                    f"tangent:{idx} with shape {t.shape} in flattened "
                    f"pytree doesn't match the shape {flat_primals_shape[idx]} "
                    "of the corresponding primal."
                )
                raise RuntimeError(msg)

            if t.device != flat_primals_device[idx]:
                msg = (
                    f"tangent:{idx} with device {t.device} in flattened "
                    f"pytree doesn't match the device {flat_primals_device[idx]} "
                    "of the corresponding primal."
                )
                raise RuntimeError(msg)

            if t.dtype != flat_primals_dtype[idx]:
                msg = (
                    f"tangent:{idx} with dtype {t.dtype} in flattened "
                    f"pytree doesn't match the dtype {flat_primals_dtype[idx]} "
                    "of the corresponding primal."
                )
                raise RuntimeError(msg)

    # jvp_fn : callable to return
    #   It takes care of checking the argspec of tangents,
    #   calling the folded fx graph and unflattening fx graph output
    def jvp_fn(*tangents):
        flat_tangents, tangent_argspec = tree_flatten(tangents)
        if tangent_argspec != primals_argspec:
            raise RuntimeError(
                f"Expected the tangents {tangent_argspec} to have "
                f"the same argspec as the primals {primals_argspec}"
            )

        forward_ad_checks(flat_tangents)

        flat_output = const_folded_jvp_graph(*flat_tangents)
        # const folded graph can return flat output,
        # so transform output.
        return tree_unflatten(flat_output, output_spec)

    return output, jvp_fn
