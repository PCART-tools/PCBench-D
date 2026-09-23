def python_call_stack(frames_to_skip: int = 0, frames_to_log: int = 16) -> _infra.Stack:
    """Returns the current Python call stack."""
    if frames_to_skip < 0:
        raise ValueError("frames_to_skip must be non-negative")
    if frames_to_log < 0:
        raise ValueError("frames_to_log must be non-negative")
    frames_to_skip += 1  # Skip this function.
    stack = _infra.Stack()
    # Frames are returned in order of oldest to newest.
    frames = traceback.extract_stack(limit=frames_to_skip + frames_to_log)
    frames.reverse()
    stack.frames = [python_frame(frame) for frame in frames[frames_to_skip:]]
    stack.message = "Python call stack"
    return stack
