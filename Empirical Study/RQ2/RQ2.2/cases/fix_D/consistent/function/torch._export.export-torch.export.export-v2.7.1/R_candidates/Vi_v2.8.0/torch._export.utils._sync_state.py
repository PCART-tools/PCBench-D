def _sync_state(src, dst):
    assert isinstance(
        src,
        torch.nn.Module,
    ), f"Expected {src} to be a nn.Module"
    assert isinstance(
        dst,
        torch.nn.Module,
    ), f"Expected {dst} to be a nn.Module"
    # Share state (params, buffers) between modules.
    # This ensures that state mutations are visible across them.
    # Since tensor constants are not mutable, copying (without sharing) is OK.
    # Also, primitive constants are specialized, so copying (without sharing) is OK.
    dst._parameters = src._parameters
    dst._buffers = src._buffers
