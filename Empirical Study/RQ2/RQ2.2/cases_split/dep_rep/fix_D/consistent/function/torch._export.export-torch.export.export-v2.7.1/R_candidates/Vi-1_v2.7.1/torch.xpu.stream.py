def stream(stream: Optional["torch.xpu.Stream"]) -> StreamContext:
    r"""Wrap around the Context-manager StreamContext that selects a given stream.

    Arguments:
        stream (Stream): selected stream. This manager is a no-op if it's ``None``.
    """
    return StreamContext(stream)
