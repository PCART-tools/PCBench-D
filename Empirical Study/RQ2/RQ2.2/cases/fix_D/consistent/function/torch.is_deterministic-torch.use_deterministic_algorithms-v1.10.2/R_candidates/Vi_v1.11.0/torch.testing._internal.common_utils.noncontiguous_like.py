def noncontiguous_like(t):
    # Short-circuits if t is already noncontiguous
    if not t.is_contiguous():
        return t

    # Special-cases 0-dim tensors
    zero_dim = t.ndim == 0
    if zero_dim:
        t = t.unsqueeze(0)

    result = torch.repeat_interleave(t.detach(), 2, dim=-1)

    # Choose a "weird" value that won't be accessed
    if t.dtype.is_floating_point or t.dtype.is_complex:
        value = math.nan
    elif t.dtype == torch.bool:
        value = True
    else:
        value = 12

    if zero_dim:
        result[0] = value
        result.set_(result.storage(), 1, (), ())
    else:
        result[..., 1::2] = value
        strides = list(result.stride())
        strides[-1] *= 2
        result.set_(result.storage(), result.storage_offset(), t.size(), stride=tuple(strides))
    result.requires_grad_(t.requires_grad)
    return result
