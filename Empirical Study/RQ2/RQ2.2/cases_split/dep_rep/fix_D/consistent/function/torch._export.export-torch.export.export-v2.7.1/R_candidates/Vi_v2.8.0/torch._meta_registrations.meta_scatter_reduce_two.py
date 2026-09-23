@register_meta([aten.scatter_reduce.two, aten.scatter_reduce.two_out])
@out_wrapper()
def meta_scatter_reduce_two(self, dim, index, src, reduce, include_self=True):
    scatter_meta_impl(self, dim, index, src, reduce, use_new_options=True)
    return self.new_empty(self.shape)
