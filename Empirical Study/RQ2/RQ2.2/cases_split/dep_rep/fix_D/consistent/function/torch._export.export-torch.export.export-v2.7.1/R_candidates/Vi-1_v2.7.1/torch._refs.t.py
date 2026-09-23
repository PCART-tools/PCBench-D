@register_decomposition(aten.t.default)
def t(a: TensorLikeType):
    # TODO: Add sparse support
    # if a.is_sparse:
    #     sparse_dim = a.sparse_dim()
    #     dense_dim = a.dense_dim()
    #     if not (sparse_dim <= 2 and dense_dim == 0):
    #         raise RuntimeError(
    #             f"t() expects a tensor with <= 2 sparse and 0 dense dimensions, but got {sparse_dim} sparse and"
    #             f"{dense_dim} dense dimensions"
    #         )
    if a.ndim > 2:
        raise RuntimeError(
            f"t() expects a tensor with <= 2 dimensions, but self is {a.ndim}D"
        )
    return torch.transpose(a, 0, 0 if a.ndim < 2 else 1)
