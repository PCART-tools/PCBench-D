def compute_elementwise_output_logical_to_physical_perm(
    *tensors, _skip_checks=False
) -> list[int]:
    from torch.fx.experimental.symbolic_shapes import guard_size_oblivious

    if not _skip_checks and len(tensors) == 0:
        msg = "Can't compute elementwise output strides for zero tensors!"
        raise ValueError(msg)

    if not _skip_checks:
        check_same_shape(*tensors, allow_cpu_scalar_tensors=True)

    # Filters the tensors to actual tensors
    if not _skip_checks:
        tensors = tuple(
            a
            for a in tensors
            if isinstance(a, TensorLike) and not is_cpu_scalar_tensor(a)
        )

    # Short-circuits for CPU scalar case
    if len(tensors) == 0:
        return []

    # Short-circuits for shapes with zero or one dimensions
    # TODO: are these necessary?
    ndim = tensors[0].ndim
    if ndim == 0:
        return []
    if ndim == 1:
        return [0]

    # Short-circuits if contiguous or channels last, following the fake fast path.
    # This reduces the number of guards we end up making
    is_contiguous = True
    is_channels_last = True
    for t in tensors:
        is_contiguous = is_contiguous and definitely_contiguous_for_memory_format(
            t, memory_format=torch.contiguous_format
        )
        is_channels_last = is_channels_last and definitely_contiguous_for_memory_format(
            t, memory_format=torch.channels_last
        )

    if is_contiguous and not is_channels_last:
        return list(range(ndim))

    if is_channels_last and not is_contiguous:
        return [0, *list(range(2, ndim)), 1]

    shape = tensors[0].shape

    def should_swap(idx_a, idx_b):
        for tensor in tensors:
            stride_a = tensor.stride()[idx_a]
            stride_b = tensor.stride()[idx_b]

            if guard_size_oblivious(stride_a == 0) or guard_size_oblivious(
                stride_b == 0
            ):
                continue

            if guard_size_oblivious(stride_a < stride_b):
                return -1

            if guard_size_oblivious(stride_a > stride_b):
                return 1

            # stride_a == stride_b
            if guard_size_oblivious(shape[idx_a] > shape[idx_b]):
                return 1

        # Note: this case is hit if all strides are zero,
        # or all strides are equal and all dimensions have the same length
        return 0

    # The "sort" order for the permutation is back-to-front, but
    # the natural order for permutations is front-to-back.  Do the
    # sorting back-to-front and then reverse it on output.
    #
    # also, note this returns the logical to physical shape permutation
    perm = list(reversed(range(ndim)))

    # insertion sort with support for ambiguous comparisons
    for i in range(1, ndim):
        dim1 = i
        for dim0 in reversed(range(i)):
            comparison = should_swap(perm[dim0], perm[dim1])
            if comparison > 0:
                perm[dim0], perm[dim1] = perm[dim1], perm[dim0]
                dim1 = dim0
            elif comparison < 0:
                break

    return list(reversed(perm))
