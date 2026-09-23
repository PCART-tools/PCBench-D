def scatter_shape_check(self, dim, index, src_opt=None):
    from torch.fx.experimental.symbolic_shapes import guard_size_oblivious

    if guard_size_oblivious(index.numel() == 0):
        return
    torch._check(
        ensure_nonempty_dim(self.dim()) == ensure_nonempty_dim(index.dim()),
        lambda: "Index tensor must have the same number of dimensions as self tensor",
    )

    is_wrong_shape = False
    self_dims = ensure_nonempty_dim(self.dim())

    # Check: index.size(d) <= self.size(d) for all d != dim
    for d in range(self_dims):
        index_d_size = ensure_nonempty_size(index, d)
        if d == dim:
            continue
        if index_d_size > ensure_nonempty_size(self, d):
            is_wrong_shape = True
            break

    # Check: index.size(d) <= src.size(d) for all d if src is Tensor
    if not is_wrong_shape and src_opt is not None:
        for d in range(self_dims):
            index_d_size = ensure_nonempty_size(index, d)
            if index_d_size > ensure_nonempty_size(src_opt, d):
                is_wrong_shape = True
                break

    if src_opt is not None:
        torch._check(
            ensure_nonempty_dim(self.dim()) == ensure_nonempty_dim(index.dim()),
            lambda: "Index tensor must have the same number of dimensions as self tensor",
        )
        torch._check(
            not is_wrong_shape,
            lambda: f"Expected index {index.shape} to be no larger than self {self.shape}"
            + f" apart from dimension {dim} and to be no larger than src {src_opt.shape}",
        )
    else:
        torch._check(
            not is_wrong_shape,
            lambda: f"Expected index {index.shape} to be no larger than self {self.shape}"
            + f" apart from dimension {dim}",
        )
