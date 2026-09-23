def _unshard_grads(
    handle: Optional[FlatParamHandle],
) -> None:
    if handle:
        handle.unshard_grad()
