def is_non_overlapping_and_dense(a: Tensor) -> bool:
    """
    True when a tensor is non-overlapping and dense.

    A tensor is non-overlapping and dense when there exists a permutation of
    its dimensions that is contiguous.
    """

    from torch.fx.experimental.symbolic_shapes import guard_size_oblivious

    if a.is_sparse:
        return False

    # Short-circuits if the tensor is already contiguous or channels-last contiguous
    if definitely_contiguous(a) or definitely_channels_last_contiguous(a):
        return True

    # The following is equivalent to compute_non_overlapping_and_dense in TensorImpl.cpp

    # Short-circuits for tensors of rank one, which are
    # non-overlapping and "dense" if their stride is one
    if a.ndim == 1:
        return a.stride()[0] == 1

    # Checks that there exists a permutation of the strides s.t. the tensor would be contiguous
    # Sorts (length, stride) pairs by stride
    #
    # This sort is done in a size-oblivious way, which helps if we do a
    # comparison like 2048*u0 > u0; we just want this to return True
    # (and not worry about what if u0 is zero).
    class K(NamedTuple):
        size: int
        stride: int

        def __lt__(self, other):
            return guard_size_oblivious(self.stride < other.stride)

        def __gt__(self, other):
            return guard_size_oblivious(self.stride > other.stride)

        def __le__(self, other):
            return guard_size_oblivious(self.stride <= other.stride)

        def __ge__(self, other):
            return guard_size_oblivious(self.stride >= other.stride)

        def __eq__(self, other):
            return guard_size_oblivious(self.stride == other.stride)

    lengths_and_strides = sorted(map(K, a.shape, a.stride()))

    expected_stride = 1
    for length, stride in lengths_and_strides:
        if guard_size_oblivious(length == 1):
            continue

        if guard_size_oblivious(stride != expected_stride):
            return False

        expected_stride *= length

    return True
