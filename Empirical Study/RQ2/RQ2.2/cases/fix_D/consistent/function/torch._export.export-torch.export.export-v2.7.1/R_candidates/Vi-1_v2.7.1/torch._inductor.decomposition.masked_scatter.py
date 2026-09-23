@register_decomposition(aten.masked_scatter)
def masked_scatter(
    self: torch.Tensor,
    mask: torch.Tensor,
    source: torch.Tensor,
) -> torch.Tensor:
    from .codegen.common import BackendFeature, has_backend_feature

    if has_backend_feature(self.device, BackendFeature.MASKED_SCATTER_WITH_INDEX):
        # This two-step algorithm is the same as eager CUDA, for eager CPU we
        # use a 1-shot serial iteration.
        self, mask = aten.broadcast_tensors([self, mask])
        source_idx = mask.reshape(-1).cumsum(0) - 1
        self_flat, mask_flat, source_flat = (x.flatten() for x in (self, mask, source))
        result = aten._unsafe_masked_index(source_flat, mask_flat, [source_idx], 0)
        return torch.where(mask_flat, result, self_flat).view(self.shape)
    return NotImplemented
