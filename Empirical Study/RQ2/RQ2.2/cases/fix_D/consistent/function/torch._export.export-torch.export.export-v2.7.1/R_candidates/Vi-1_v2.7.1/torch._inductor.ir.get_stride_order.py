def get_stride_order(
    seq: Sequence[Union[int, torch.SymInt, Expr]], shape_env: Optional[ShapeEnv] = None
) -> Sequence[int]:
    """
    Convert strides to stride order
    """
    sorted_idx: Sequence[int] = get_fill_order(seq, shape_env)
    out = [0 for _ in range(len(seq))]
    for i, elem in enumerate(sorted_idx):
        out[elem] = i
    return out
