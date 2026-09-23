def _cpp_call_stack(frames_to_skip: int = 0, frames_to_log: int = 32) -> infra.Stack:
    """Returns the current C++ call stack.

    This function utilizes `torch.utils.cpp_backtrace` to get the current C++ call stack.
    The returned C++ call stack is a concatenated string of the C++ call stack frames.
    Each frame is separated by a newline character, in the same format of
    r"frame #[0-9]+: (?P<frame_info>.*)". More info at `c10/util/Backtrace.cpp`.

    """
    frames = cpp_backtrace.get_cpp_backtrace(frames_to_skip, frames_to_log).split("\n")
    frame_messages = []
    for frame in frames:
        segments = frame.split(":", 1)
        if len(segments) == 2:
            frame_messages.append(segments[1].strip())
        else:
            frame_messages.append("<unknown frame>")
    return infra.Stack(
        frames=[
            infra.StackFrame(location=infra.Location(message=message))
            for message in frame_messages
        ]
    )
