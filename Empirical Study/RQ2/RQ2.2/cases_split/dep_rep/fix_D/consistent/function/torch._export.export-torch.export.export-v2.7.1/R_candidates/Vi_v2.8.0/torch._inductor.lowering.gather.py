@register_lowering(aten.gather, type_promotion_kind=None)
def gather(x, dim, index, sparse_grad=False):
    # sparse_grad doesn't affect forward computation,
    # and backward tracing is taken care of by AOT Autograd
    assert isinstance(x, TensorBox)
    if index.get_numel() == 0:
        # Empty index case. Return an empty array with the same shape
        return new_empty(x, index.get_size())

    size = x.get_size()
    offset = len(size) == 0
    dim = _validate_dim(x, dim, offset)

    if offset:
        x = expand(x, [1])
        size = [1]

    x_loader = x.make_loader()
    index_loader = index.make_loader()

    def fn(idx):
        idx = list(idx)
        gather_idx = ops.indirect_indexing(index_loader(idx), size[dim])
        if len(idx) == 0:
            idx = [gather_idx]
        else:
            idx[dim] = gather_idx
        return x_loader(idx)

    return Pointwise.create(
        device=x.get_device(),
        dtype=x.get_dtype(),
        inner_fn=fn,
        ranges=index.get_size(),
    )
