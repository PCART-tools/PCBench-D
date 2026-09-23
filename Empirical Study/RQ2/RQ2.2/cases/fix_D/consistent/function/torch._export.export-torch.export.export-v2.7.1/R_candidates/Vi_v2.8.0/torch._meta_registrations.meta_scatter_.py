@register_meta(
    [
        aten.scatter_.src,
        aten.scatter_.value,
        aten.scatter_.reduce,
        aten.scatter_.value_reduce,
    ]
)
def meta_scatter_(self, dim, index, src_or_value, reduce=None):
    src = src_or_value if isinstance(src_or_value, torch.Tensor) else None
    scatter_meta_impl(self, dim, index, src, reduce)
    return self
