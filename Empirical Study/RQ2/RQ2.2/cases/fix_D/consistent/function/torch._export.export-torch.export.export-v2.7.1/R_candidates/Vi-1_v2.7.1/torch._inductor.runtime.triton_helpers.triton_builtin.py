def triton_builtin(f: _T) -> _T:
    """
    Decorator to mark a function as a Triton built-in function.  These functions
    are evaluated at compile time.

    Args:
        f (function): The function to be marked as a Triton built-in.

    Returns:
        function: The same function, marked as a Triton built-in.
    """
    f.__triton_builtin__ = True  # type: ignore[attr-defined]
    return f
