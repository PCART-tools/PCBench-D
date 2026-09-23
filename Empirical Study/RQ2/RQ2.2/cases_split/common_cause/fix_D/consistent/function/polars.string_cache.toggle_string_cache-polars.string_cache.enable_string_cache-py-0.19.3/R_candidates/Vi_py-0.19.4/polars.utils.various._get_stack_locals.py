def _get_stack_locals(
    of_type: type | tuple[type, ...] | None = None,
    n_objects: int | None = None,
    n_frames: int | None = None,
    named: str | tuple[str, ...] | None = None,
) -> dict[str, Any]:
    """
    Retrieve f_locals from all (or the last 'n') stack frames from the calling location.

    Parameters
    ----------
    of_type
        Only return objects of this type.
    n_objects
        If specified, return only the most recent ``n`` matching objects.
    n_frames
        If specified, look at objects in the last ``n`` stack frames only.
    named
        If specified, only return objects matching the given name(s).

    """
    if isinstance(named, str):
        named = (named,)

    objects = {}
    examined_frames = 0
    if n_frames is None:
        n_frames = sys.maxsize
    stack_frame = inspect.currentframe()
    stack_frame = getattr(stack_frame, "f_back", None)

    try:
        while stack_frame and examined_frames < n_frames:
            local_items = list(stack_frame.f_locals.items())
            for nm, obj in reversed(local_items):
                if (
                    nm not in objects
                    and (named is None or (nm in named))
                    and (of_type is None or isinstance(obj, of_type))
                ):
                    objects[nm] = obj
                    if n_objects is not None and len(objects) >= n_objects:
                        return objects

            stack_frame = stack_frame.f_back
            examined_frames += 1
    finally:
        # https://docs.python.org/3/library/inspect.html
        # > Though the cycle detector will catch these, destruction of the frames
        # > (and local variables) can be made deterministic by removing the cycle
        # > in a finally clause.
        del stack_frame

    return objects
