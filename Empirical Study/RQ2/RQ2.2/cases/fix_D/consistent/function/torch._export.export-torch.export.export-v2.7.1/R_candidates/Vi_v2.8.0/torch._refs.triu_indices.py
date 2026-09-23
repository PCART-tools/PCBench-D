@register_decomposition(aten.triu_indices)
@out_wrapper()
def triu_indices(
    row: int,
    col: int,
    offset: int = 0,
    *,
    dtype: torch.dtype = torch.long,
    layout: torch.layout = torch.strided,
    device: DeviceLikeType = "cpu",
    pin_memory: bool = False,
) -> TensorLikeType:
    _trilu_checks("triu_indices", row, col, dtype, layout, pin_memory)

    trapezoid_size, rectangle_size, m_first_row = _get_triu_sizes(row, col, offset)
    col_offset = max(0, offset)

    arange_kw = partial(
        torch.arange, layout=layout, device=device, pin_memory=pin_memory
    )

    # indices for top rectangle
    xs2 = arange_kw(0, rectangle_size, dtype=dtype)
    row_inds2 = xs2 // col
    col_inds2 = xs2 % col

    # bottom trapezoid
    xs1 = arange_kw(0, trapezoid_size, dtype=torch.float64)
    b = -0.5 - m_first_row
    row_inds1 = torch.floor(-b - torch.sqrt(b * b - 2 * xs1))
    col_inds1 = torch.floor(xs1 - ((2 * m_first_row - 1 - row_inds1) * row_inds1) * 0.5)
    row_inds1 = _maybe_convert_to_dtype(row_inds1, dtype)
    col_inds1 = _maybe_convert_to_dtype(col_inds1, dtype)

    if col:
        row_inds1 = row_inds1 + (rectangle_size // col)
    col_inds1 = col_inds1 + col_offset

    return torch.stack(
        (torch.cat((row_inds2, row_inds1)), torch.cat((col_inds2, col_inds1)))
    )
