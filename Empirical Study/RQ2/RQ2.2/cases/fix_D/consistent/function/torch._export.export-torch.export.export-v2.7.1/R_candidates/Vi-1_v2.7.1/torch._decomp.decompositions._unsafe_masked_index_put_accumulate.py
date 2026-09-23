@register_decomposition([aten._unsafe_masked_index_put_accumulate])
def _unsafe_masked_index_put_accumulate(x, mask, indices, values):
    for index in indices:
        if index is not None:
            torch._check(
                index.dtype in [torch.long, torch.int],
                lambda: "tensors used as indices must be long or int tensors",
            )

    torch._check(
        mask.dtype == torch.bool,
        lambda: "tensors used as masks must be bool tensors",
    )

    if x.numel() == 0:
        return x.clone()

    for i in range(len(indices)):
        index = indices[i]
        if index is not None:
            indices[i] = index.clamp(min=-x.size(i), max=x.size(i) - 1)

    masked_value = values.masked_fill(~mask, 0)
    return aten._unsafe_index_put(x, indices, masked_value, accumulate=True)
