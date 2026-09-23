@register_meta(aten.gather.default)
def meta_gather(self, dim, index, sparse_grad=False):
    from torch.fx.experimental.symbolic_shapes import guard_size_oblivious

    wrapped_dim = maybe_wrap_dim(dim, self.dim())
    is_index_empty = guard_size_oblivious(index.numel() == 0)
    if not is_index_empty:
        torch._check(
            index.dtype == torch.long or index.dtype == torch.int,
            lambda: f"gather(): Expected dtype int32/int64 for index, but got {index.dtype}",
        )
        gather_shape_check(self, wrapped_dim, index)
    return self.new_empty(index.shape)
