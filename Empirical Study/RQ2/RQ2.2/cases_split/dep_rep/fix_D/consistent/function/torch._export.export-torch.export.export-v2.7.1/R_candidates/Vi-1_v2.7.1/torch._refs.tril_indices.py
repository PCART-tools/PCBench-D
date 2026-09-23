@register_decomposition(aten.tril_indices)
@out_wrapper()
def tril_indices(
    row: int,
    col: int,
    offset: int = 0,
    *,
    dtype: torch.dtype = torch.long,
    layout: torch.layout = torch.strided,
    device: DeviceLikeType = "cpu",
    pin_memory: bool = False,
) -> TensorLikeType:
    _trilu_checks("tril_indices", row, col, dtype, layout, pin_memory)

    trapezoid_size, rectangle_size, m_first_row = _get_tril_sizes(row, col, offset)
    row_offset = max(0, -offset)

    arange_kw = partial(
        torch.arange, layout=layout, device=device, pin_memory=pin_memory
    )

    # first we do the indices for top trapezoid
    xs1 = arange_kw(0, trapezoid_size, dtype=torch.float64)
    b = m_first_row - 0.5
    row_inds1 = torch.floor(-b + torch.sqrt(b * b + 2 * xs1))
    col_inds1 = torch.floor(xs1 - (2 * m_first_row - 1 + row_inds1) * row_inds1 * 0.5)
    row_inds1 = _maybe_convert_to_dtype(row_inds1 + row_offset, dtype)
    col_inds1 = _maybe_convert_to_dtype(col_inds1, dtype)

    # then bottom rectangle
    xs2 = arange_kw(0, rectangle_size, dtype=dtype)
    row_inds2 = xs2 // col + (col - m_first_row + 1 + row_offset)
    col_inds2 = xs2 % col

    return torch.stack(
        (torch.cat((row_inds1, row_inds2)), torch.cat((col_inds1, col_inds2)))
    )
