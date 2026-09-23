def _derive_module_name(depth: int = 1) -> Optional[str]:
    """
    Derives the name of the caller module from the stack frames.

    Args:
        depth: The position of the frame in the stack.
    """
    try:
        stack = inspect.stack()
        assert depth < len(stack)
        # FrameInfo is just a named tuple: (frame, filename, lineno, function, code_context, index)
        frame_info = stack[depth]

        module = inspect.getmodule(frame_info[0])
        if module:
            module_name = module.__name__
        else:
            # inspect.getmodule(frame_info[0]) does NOT work (returns None) in
            # binaries built with @mode/opt
            # return the filename (minus the .py extension) as modulename
            filename = frame_info[1]
            module_name = os.path.splitext(os.path.basename(filename))[0]
        return module_name
    except Exception as e:
        warnings.warn(
            f"Error deriving logger module name, using <None>. Exception: {e}",
            RuntimeWarning,
        )
        return None
