@register_meta(
    [
        aten.scatter.src,
        aten.scatter.value,
        aten.scatter.reduce,
        aten.scatter.value_reduce,
    ]
)
@out_wrapper()
def meta_scatter(self, dim, index, src_or_value, reduce=None):
    src = src_or_value if isinstance(src_or_value, torch.Tensor) else None
    scatter_meta_impl(self, dim, index, src, reduce)
    return self.new_empty(self.shape)
