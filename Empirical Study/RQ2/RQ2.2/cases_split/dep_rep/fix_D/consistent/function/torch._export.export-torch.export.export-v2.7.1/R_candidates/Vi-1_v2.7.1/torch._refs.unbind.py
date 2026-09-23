@register_decomposition(aten.unbind)
def unbind(t: TensorLikeType, dim: int = 0) -> TensorSequenceType:
    from torch.fx.experimental.symbolic_shapes import guard_size_oblivious

    dim = utils.canonicalize_dim(t.ndim, dim)
    torch._check_index(
        len(t.shape) > 0,
        lambda: "Dimension specified as 0 but tensor has no dimensions",
    )
    if guard_size_oblivious(t.shape[dim] == 0):
        return ()
    else:
        return tuple(
            torch.squeeze(s, dim) for s in torch.tensor_split(t, t.shape[dim], dim)
        )
