def _reshape_view_helper(a: TensorLikeType, *shape, allow_copy: bool) -> TensorLikeType:
    from torch.fx.experimental.symbolic_shapes import guard_size_oblivious, sym_eq

    # Creates a valid shape
    shape = utils.extract_shape_from_varargs(shape, validate=False)
    # Reshape may be given a shape with a -1 length
    # This indicates that the dimension's length should be inferred
    shape = utils.infer_size(shape, a.numel())

    # Special-cases tensors with no elements
    if guard_size_oblivious(a.numel() == 0):
        return as_strided(a, shape, utils.make_contiguous_strides_for(shape))

    # Special-cases reshaping zero dim tensors
    if a.ndim == 0:
        _a = a
        for length in shape:
            assert length == 1
            _a = unsqueeze(_a, -1)
        if _a is a:
            return prims.view_of(a)
        else:
            return _a

    # Special-cases reshaping to zero dim tensors
    if len(shape) == 0:
        _a = a
        for length in a.shape:
            assert length == 1
            _a = squeeze(_a, -1)
        if _a is a:
            return prims.view_of(a)
        else:
            return _a

    if a.is_contiguous():
        # Special-cases for nd_to_1d
        if len(shape) == 1 and a.ndim > 1:
            return torch.as_strided(a, [a.numel()], [1])
        # Special-cases for 1d_to_2d
        if len(shape) == 2 and a.ndim == 1:
            dim0 = shape[0]
            dim1 = shape[1]
            return torch.as_strided(a, [dim0, dim1], [dim1, 1])

    # Handles general case: a 1+D tensor reshaped into a distinct 1+D shape

    # NOTE [Reshape Algorithm]
    # This algorithm works by attempting to greedily construct the desired dimensions in
    # the output shape, left to right. It does this by, conceptually, accumulating
    # dimensions of the original tensor, also left to right, until the dimension
    # can be constructed using prims.split_dim.
    # The algorithm also has special handling for tail squeezes/unsqueezes, like
    # if a reshape from (5, 5) to (5, 5, 1) or vice versa.
    #
    # This algorithm does not flatten the original tensor and then split dims as appropriate
    # because that would create copies more often than this algorithm. flatten is the only
    # operation below which can create a view or a copy, and while it prefers creating
    # views it may sometimes create a copy if the tensor's strides do not permit a view.
    # As a result, this algorithm tries to minimize flattening.
    #
    # Note that a better version of this algorithm may exist. Regions which could be
    # flattened without creating a copy can be identified in advance, and that might
    # allow fewer flatten calls or faster short-circuiting to make a copy.
    idx = 0
    a_ = a
    for length in shape:
        # Handles tail unsqueezes
        if idx >= a_.ndim:
            assert length == 1
            last_dim = a_.ndim - 1
            # NOTE: using split_dim instead of unsqueeze may seem silly here,
            # but it's necessary to get the strides correct
            a_ = prims.split_dim(a_, last_dim, a_.shape[last_dim])
            idx = idx + 1
            continue

        # Skips dimensions that are already the correct length
        if guard_size_oblivious(length == a_.shape[idx]):
            idx = idx + 1
            continue

        # Gathers enough original dimensions such that this new dimension can be created
        # Note that this accumulation will terminate because we've verified a and the shape
        # specify the same number of elements above
        accum = a_.shape[idx]
        end = idx
        while guard_size_oblivious(accum % length != 0):
            end = end + 1
            accum = accum * a_.shape[end]
        if end != idx:
            # NOTE: in this case multiple dimensions must be flatten to create the desired dimension
            # This flattening is why reshape sometimes creates a copy -- because flattening
            # may return a view of a copy

            # Checks if collapse can be a view and short-circuits to copying reshape if it can't
            new_shape, _new_strides = prims._collapse_view_helper(a_, idx, end)
            if new_shape is None:
                if allow_copy:
                    return prims.reshape(a, shape)

                msg = f"Cannot view a tensor with shape {a.shape} and strides {a.stride()} as a tensor with shape {shape}!"
                raise ValueError(msg)

            a_ = flatten(a_, idx, end)

        # Splits the (possibly flattened) dimension to create the desired dim length
        if guard_size_oblivious(accum != length):
            a_ = prims.split_dim(a_, idx, length)

        idx = idx + 1

    # Squeezes tail
    while idx < a_.ndim:
        torch._check(
            a_.shape[idx] == 1,
            lambda: f"a.size({idx}) expected to be 1 but got {a_.shape[idx]}",
        )
        a_ = squeeze(a_, idx)

    if a_ is a:
        return prims.view_of(a)
    else:
        return a_
