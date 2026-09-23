@register_meta([aten.kthvalue.default, aten.kthvalue.values])
@out_wrapper("values", "indices")
def kthvalue_meta(self, k, dim=-1, keepdim=False):
    dim = maybe_wrap_dim(dim, self.dim(), wrap_scalar=True)
    dimSize = self.size(dim) if self.dim() > 0 else 1
    torch._check(
        k >= 1 and k <= dimSize,
        lambda: f"kthvalue(): selected number k out of range for dimension {dim}",
    )

    shape = list(self.shape[:dim] + self.shape[dim + 1 :])
    if keepdim and self.dim() > 0:
        shape.insert(dim, 1)
    return self.new_empty(shape), self.new_empty(shape, dtype=torch.int64)
