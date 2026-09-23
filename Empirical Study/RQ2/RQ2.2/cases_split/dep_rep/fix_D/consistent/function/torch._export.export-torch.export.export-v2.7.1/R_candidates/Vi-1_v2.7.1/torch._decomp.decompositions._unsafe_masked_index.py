@register_decomposition([aten._unsafe_masked_index])
def _unsafe_masked_index(x, mask, indices, fill):
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

    from torch.fx.experimental.symbolic_shapes import guard_size_oblivious

    if guard_size_oblivious(x.numel() == 0):
        meta_result = torch._meta_registrations.meta_index_Tensor(x, indices)
        return x.new_full(meta_result.shape, fill)

    for i in range(len(indices)):
        index = indices[i]
        if index is not None:
            indices[i] = index.clamp(min=0, max=x.size(i) - 1)

    return aten._unsafe_index(x, indices).masked_fill(~mask, fill)
