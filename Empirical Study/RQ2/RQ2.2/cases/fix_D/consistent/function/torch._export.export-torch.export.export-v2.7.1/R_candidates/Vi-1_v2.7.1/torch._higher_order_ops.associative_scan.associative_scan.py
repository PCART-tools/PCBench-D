def associative_scan(
    combine_fn: Callable[[pytree.PyTree, pytree.PyTree], pytree.PyTree],
    xs: pytree.PyTree,
    dim: int,
    reverse: bool = False,
    combine_mode: str = "pointwise",
) -> torch.Tensor:
    r"""
    Performs an inclusive scan with an associative combine function.

    .. warning::
        `torch.associative_scan` is a prototype feature in PyTorch. It currently
        does not support autograd and you may run into miscompiles.
        Read more about feature classification at:
        https://pytorch.org/blog/pytorch-feature-classification-changes/#prototype

    This operator requires runtime code generation and so requires support for
    ``torch.compile``. Further, only CUDA device codegen is supported at the moment.

    Args:
        combine_fn (Callable): A binary callable with type ``(Tensor, Tensor) -> Tensor``,
            or if input is a pytree ``(pytree, pytree) -> pytree``.
            This function must be pure, i.e., no lifted arguments are supported at the moment,
            satisfy the associative property and have no side-effects.
        xs (torch.Tensor): The input tensor, or nested pytree of tensors.
            All inputs are expected to have the same shape.
        dim (int): the dimension to scan over
        reverse (bool): A boolean stating if the scan should be reversed with respect to ``dim``, default ``False``.
        combine_mode (str): A string indicating whether the ``combine_fn`` is ``pointwise`` or ``generic``, default ``pointwise``.
            If ``combine_mode=pointwise``, ``combine_fn`` must be pure, may only contain pointwise operations
            and ``xs`` must be CUDA tensors.
            In all other cases ``combine_mode=generic`` should be used.
            Note: ``combine_mode=pointwise`` is more efficient than ``combine_mode=generic``.


    Example::

        def add(x: torch.Tensor, y: torch.Tensor):
            return x + y

        cumsum = associative_scan(add, x, dim)

    """
    if not callable(combine_fn):
        raise ValueError("Combine_fn must be a callable, but got {combine_fn}")
    if not isinstance(dim, int):
        raise ValueError("Dim must be an int, but got " + str(type(dim)))
    if combine_mode not in ["pointwise", "generic"]:
        raise ValueError(
            "Combine_mode must either 'pointwise' or 'generic', but got {combine_mode}"
        )

    if not torch.compiler.is_compiling():
        with _set_compilation_env(), torch._dynamo.utils.disable_cache_limit():
            return torch.compile(associative_scan, fullgraph=True, backend="eager")(
                combine_fn, xs, dim, reverse=reverse, combine_mode=combine_mode
            )

    leaves, spec = pytree.tree_flatten(xs)

    if combine_mode == "pointwise" and not all(l.device.type == "cuda" for l in leaves):
        raise ValueError(
            "For combine_mode='pointwise', all input tensors need to be on CUDA"
        )

    if len(leaves) == 0:
        raise ValueError("Expected at least 1 xs leaf")
    if any(not isinstance(x, torch.Tensor) for x in leaves):
        raise ValueError("xs leaves must be a Tensor")
    if any(x.is_sparse for x in leaves):
        raise ValueError("xs leaves must dense Tensors, consider using `to_dense()`")
    if any(x.ndim <= dim for x in leaves):
        raise ValueError(
            "All xs leaves must at least have 'dim' number of dimensions and scan dimension > 0"
        )
    if any(x.shape[dim] == 0 for x in leaves):
        raise ValueError(
            "All xs leaves must at least have 'dim' number of dimensions and scan dimension > 0"
        )

    if reverse:
        leaves = [torch.flip(elem, [dim]) for elem in leaves]

    ndim = leaves[0].ndim
    orig_scan_dim = utils.canonicalize_dim(ndim, dim)
    leaves = [torch.movedim(elem, dim, 0) for elem in leaves]

    # Call the combine_fn with only a slice along the scan dim
    # and check whether the output leaves have the same slice dimensions
    sliced_leaves = [first_slice_copy(leaf) for leaf in leaves]

    out = combine_fn(
        pytree.tree_unflatten(sliced_leaves, spec),
        pytree.tree_unflatten(sliced_leaves, spec),
    )
    out_leaves = pytree.tree_leaves(out)
    if len(leaves) != len(out_leaves):
        raise RuntimeError(
            "The number of leaves of the pytree of the output of the operator needs to match the length of the pytree of the input"
        )
    if any(
        x.shape != x_sliced.shape
        or x.dtype != x_sliced.dtype
        or x.device != x_sliced.device
        or x.stride() != x_sliced.stride()
        for x, x_sliced in zip(out_leaves, sliced_leaves)
    ):
        raise RuntimeError(
            f"The metadata of the output of the operator needs to match the meta data of the xs pytree"
            f"\n  xs metadata             : {[(x.shape, x.dtype, x.device, x.stride()) for x in sliced_leaves]}"
            f"\n  operator output metadata: {[(x.shape, x.dtype, x.device, x.stride()) for x in out_leaves]}"
        )

    if combine_mode == "generic":
        # The generic_associative_scan implementation calls the combine_fn with a `batch` along the scan dimension
        # For example, consider:
        # def add(x: torch.Tensor, y: torch.Tensor):
        #     return x + y
        # leaves = torch.tensor([[0.0, 1.0, 2.0, 3.0]
        #                        [0.0, 1.0, 2.0, 3.0]])
        # which has shape 2 x 4;
        # dim = 1;
        # In the first iteration of `_scan` the combine_fn gets invoked with
        # combine_fn([torch.tensor([[0.0, 2.0],
        #                           [0.0, 2.0]])],
        #            [torch.tensor([[1.0, 3.0],
        #                           [1.0, 3.0]])])
        # The arguments are of shape 2 x 2, but can be evaluated in parallel along the scan dimension.
        combine_fn = functools.partial(
            wrap_combine_fn_flat,
            combine_fn=torch.vmap(
                combine_fn,
                in_dims=(
                    pytree.tree_unflatten([0] * len(leaves), spec),
                    pytree.tree_unflatten([0] * len(leaves), spec),
                ),
                out_dims=0,
            ),
            spec=spec,
            num_leaves=len(leaves),
        )
        result_flat = generic_associative_scan(combine_fn, leaves, additional_inputs=())
    else:
        combine_fn = functools.partial(
            wrap_combine_fn_flat,
            combine_fn=combine_fn,
            spec=spec,
            num_leaves=len(leaves),
        )
        result_flat = associative_scan_op(combine_fn, leaves, additional_inputs=())

    if reverse:
        result_flat = [torch.flip(elem, [0]) for elem in result_flat]

    result_flat = [torch.movedim(elem, 0, orig_scan_dim) for elem in result_flat]

    return pytree.tree_unflatten(result_flat, spec)
