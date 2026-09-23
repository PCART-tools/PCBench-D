@register_lowering(aten._unsafe_masked_index, type_promotion_kind=None)
def _unsafe_masked_index(self, mask, indices, fill):
    ranges, _, _unsafe_index_fn = index_impl_helper(
        self, indices, check=False, wrap_neg=False
    )
    mask_loader = mask.make_loader()
    self_loader = self.make_loader()

    def inner_fn(idx):
        if mask.dtype != torch.bool:
            mask_val = ops.to_dtype(mask_loader(idx), torch.bool)
        else:
            mask_val = mask_loader(idx)
        return ops.masked(mask_val, lambda: self_loader(_unsafe_index_fn(idx)), fill)

    return Pointwise.create(
        device=self.get_device(),
        dtype=self.get_dtype(),
        inner_fn=inner_fn,
        ranges=ranges,
    )
