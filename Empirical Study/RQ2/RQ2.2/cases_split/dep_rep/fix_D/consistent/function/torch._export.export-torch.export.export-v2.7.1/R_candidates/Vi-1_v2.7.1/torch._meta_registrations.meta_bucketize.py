@register_meta([aten.bucketize.Tensor, aten.bucketize.Tensor_out])
@out_wrapper()
def meta_bucketize(self, boundaries, *, out_int32=False, right=False):
    return torch.empty_like(
        self,
        dtype=torch.int32 if out_int32 else torch.int64,
        memory_format=torch.contiguous_format,
    )
