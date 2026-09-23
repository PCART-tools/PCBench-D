def dims(
    *names: str, min: Optional[int] = None, max: Optional[int] = None
) -> tuple[Dim, ...]:
    """
    Util to create multiple :func:`Dim` types.

    Returns:
        A tuple of :func:`Dim` types.
    """
    return tuple(Dim(name, min=min, max=max) for name in names)  # type: ignore[misc]
