def unpack_int8_to_int4(weight):
    assert weight.dim() == 2
    assert weight.dtype == torch.int8
    return torch.stack((weight & 0xF, (weight >> 4) & 0xF), dim=2).view(
        weight.shape[0], 2 * weight.shape[1]
    )
