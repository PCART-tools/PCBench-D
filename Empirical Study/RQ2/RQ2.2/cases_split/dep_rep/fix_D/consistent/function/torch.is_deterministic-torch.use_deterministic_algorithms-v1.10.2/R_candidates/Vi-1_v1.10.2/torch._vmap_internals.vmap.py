def vmap(func: Callable, in_dims: in_dims_t = 0, out_dims: out_dims_t = 0) -> Callable:
    """
    vmap is the vectorizing map. Returns a new function that maps `func` over some
    dimension of the inputs. Semantically, vmap pushes the map into PyTorch
    operations called by `func`, effectively vectorizing those operations.

    vmap is useful for handling batch dimensions: one can write a function `func`
    that runs on examples and then lift it to a function that can take batches of
    examples with `vmap(func)`. vmap can also be used to compute batched
    gradients when composed with autograd.

    .. note::
        We are actively developing a different and improved vmap prototype
        `here. <https://github.com/zou3519/functorch>`_ The improved
        prototype is able to arbitrarily compose with gradient computation.
        Please give that a try if that is what you're looking for.

        Furthermore, if you're interested in using vmap for your use case,
        please `contact us! <https://github.com/pytorch/pytorch/issues/42368>`_
        We're interested in gathering feedback from early adopters to inform
        the design.

    .. warning::
        torch.vmap is an experimental prototype that is subject to
        change and/or deletion. Please use at your own risk.

    Args:
        func (function): A Python function that takes one or more arguments.
            Must return one or more Tensors.
        in_dims (int or nested structure): Specifies which dimension of the
            inputs should be mapped over. `in_dims` should have a structure
            like the inputs. If the `in_dim` for a particular input is None,
            then that indicates there is no map dimension. Default: 0.
        out_dims (int or Tuple[int]): Specifies where the mapped dimension
            should appear in the outputs. If `out_dims` is a Tuple, then it should
            have one element per output. Default: 0.

    Returns:
        Returns a new "batched" function. It takes the same inputs as `func`,
        except each input has an extra dimension at the index specified by `in_dims`.
        It takes returns the same outputs as `func`, except each output has
        an extra dimension at the index specified by `out_dims`.

    .. warning:
        vmap works best with functional-style code. Please do not perform any
        side-effects in `func`, with the exception of in-place PyTorch operations.
        Examples of side-effects include mutating Python data structures and
        assigning values to variables not captured in `func`.

    One example of using `vmap` is to compute batched dot products. PyTorch
    doesn't provide a batched `torch.dot` API; instead of unsuccessfully
    rummaging through docs, use `vmap` to construct a new function.

        >>> torch.dot                            # [D], [D] -> []
        >>> batched_dot = torch.vmap(torch.dot)  # [N, D], [N, D] -> [N]
        >>> x, y = torch.randn(2, 5), torch.randn(2, 5)
        >>> batched_dot(x, y)

    `vmap` can be helpful in hiding batch dimensions, leading to a simpler
    model authoring experience.

        >>> batch_size, feature_size = 3, 5
        >>> weights = torch.randn(feature_size, requires_grad=True)
        >>>
        >>> def model(feature_vec):
        >>>     # Very simple linear model with activation
        >>>     return feature_vec.dot(weights).relu()
        >>>
        >>> examples = torch.randn(batch_size, feature_size)
        >>> result = torch.vmap(model)(examples)

    `vmap` can also help vectorize computations that were previously difficult
    or impossible to batch. One example is higher-order gradient computation.
    The PyTorch autograd engine computes vjps (vector-Jacobian products).
    Computing a full Jacobian matrix for some function f: R^N -> R^N usually
    requires N calls to `autograd.grad`, one per Jacobian row. Using `vmap`,
    we can vectorize the whole computation, computing the Jacobian in a single
    call to `autograd.grad`.

        >>> # Setup
        >>> N = 5
        >>> f = lambda x: x ** 2
        >>> x = torch.randn(N, requires_grad=True)
        >>> y = f(x)
        >>> I_N = torch.eye(N)
        >>>
        >>> # Sequential approach
        >>> jacobian_rows = [torch.autograd.grad(y, x, v, retain_graph=True)[0]
        >>>                  for v in I_N.unbind()]
        >>> jacobian = torch.stack(jacobian_rows)
        >>>
        >>> # vectorized gradient computation
        >>> def get_vjp(v):
        >>>     return torch.autograd.grad(y, x, v)
        >>> jacobian = torch.vmap(get_vjp)(I_N)

    .. note::
        vmap does not provide general autobatching or handle variable-length
        sequences out of the box.
    """
    warnings.warn(
        'torch.vmap is an experimental prototype that is subject to '
        'change and/or deletion. Please use at your own risk. There may be '
        'unexpected performance cliffs due to certain operators not being '
        'implemented. To see detailed performance warnings please use '
        '`torch._C._debug_only_display_vmap_fallback_warnings(True) '
        'before the call to `vmap`.',
        stacklevel=2)
    return _vmap(func, in_dims, out_dims)
