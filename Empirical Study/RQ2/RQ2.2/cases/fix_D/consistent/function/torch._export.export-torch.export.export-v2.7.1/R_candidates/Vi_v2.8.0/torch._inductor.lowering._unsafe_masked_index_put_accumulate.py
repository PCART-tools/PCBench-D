@register_lowering(aten._unsafe_masked_index_put_accumulate, type_promotion_kind=None)
def _unsafe_masked_index_put_accumulate(x, mask, indices, values):
    masked_value = where(mask, values, 0)
    shape = x.get_size()
    clamped_indices = [
        clamp(indices[i], -shape[i], shape[i] - 1) if indices[i] else None
        for i in range(len(indices))
    ]
    # TODO: use a masked store for this. currently only triton
    # supports masked stores and cpp backend does not.
    return _unsafe_index_put(x, clamped_indices, masked_value, accumulate=True)
