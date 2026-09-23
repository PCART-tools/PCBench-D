def collate_numpy_scalar_fn(
    batch,
    *,
    collate_fn_map: Optional[dict[Union[type, tuple[type, ...]], Callable]] = None,
):
    return torch.as_tensor(batch)
