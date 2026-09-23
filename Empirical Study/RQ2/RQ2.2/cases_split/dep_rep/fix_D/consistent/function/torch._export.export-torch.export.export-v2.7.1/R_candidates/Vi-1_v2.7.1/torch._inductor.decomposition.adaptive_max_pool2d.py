@register_decomposition(aten.adaptive_max_pool2d)
def adaptive_max_pool2d(
    x: torch.Tensor, output_size: list[int]
) -> tuple[torch.Tensor, torch.Tensor]:
    *batch, h_in, w_in = x.shape
    h_out, w_out = output_size

    if h_out == 0 or w_out == 0:
        o_size = [*batch, h_out, w_out]
        return x.new_empty(o_size), x.new_empty(o_size, dtype=torch.int64)

    if h_in % h_out == 0 and w_in % w_out == 0:
        kernel_size = [h_in // h_out, w_in // w_out]
        return aten.max_pool2d_with_indices(x, kernel_size)

    return NotImplemented
