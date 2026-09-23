def stream(stream: Optional["torch.cuda.Stream"]) -> StreamContext:
    r"""Wrap around the Context-manager StreamContext that selects a given stream.

    Arguments:
        stream (Stream): selected stream. This manager is a no-op if it's
            ``None``.
    .. note::
        In eager mode stream is of type Stream class while in JIT it is
        an object of the custom class ``torch.classes.cuda.Stream``.
    """
    return StreamContext(stream)
