def _reshard_grads(
    handle: Optional[FlatParamHandle],
) -> None:
    if handle:
        handle.reshard_grad()
