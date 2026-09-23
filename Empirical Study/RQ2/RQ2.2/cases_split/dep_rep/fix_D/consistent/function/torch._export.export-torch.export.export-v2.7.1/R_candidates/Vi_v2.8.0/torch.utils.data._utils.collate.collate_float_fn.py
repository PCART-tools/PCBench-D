def collate_float_fn(
    batch,
    *,
    collate_fn_map: Optional[dict[Union[type, tuple[type, ...]], Callable]] = None,
):
    return torch.tensor(batch, dtype=torch.float64)
