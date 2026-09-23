@register_rng_decomposition(aten.rand)
def rand(shape, dtype=None, layout=torch.strided, device=None, pin_memory=False):
    if device and device.type != "cuda":
        throw_on_non_cuda(device)
    seed, offset = PhiloxStateTracker.get_state_as_tuple()
    dtype = dtype or torch.float32
    out, offset_jump = torch.ops.rngprims.philox_rand(
        shape, seed, offset, None, device, dtype
    )
    PhiloxStateTracker.advance_offset(offset_jump)
    return out
