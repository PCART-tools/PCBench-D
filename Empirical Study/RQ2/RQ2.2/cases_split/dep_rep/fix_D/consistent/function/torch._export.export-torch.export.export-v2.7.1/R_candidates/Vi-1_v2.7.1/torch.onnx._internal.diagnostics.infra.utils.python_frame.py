def python_frame(frame: traceback.FrameSummary) -> _infra.StackFrame:
    """Returns a StackFrame for the given traceback.FrameSummary."""
    snippet = frame.line

    return _infra.StackFrame(
        location=_infra.Location(
            uri=frame.filename,
            line=frame.lineno,
            snippet=snippet,
            function=frame.name,
            message=snippet,
        )
    )
