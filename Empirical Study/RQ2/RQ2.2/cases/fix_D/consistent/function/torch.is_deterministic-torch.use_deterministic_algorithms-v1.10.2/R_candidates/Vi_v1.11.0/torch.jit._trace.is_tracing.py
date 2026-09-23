def is_tracing():
    """
    Returns ``True`` in tracing (if a function is called during the tracing of
    code with ``torch.jit.trace``) and ``False`` otherwise.
    """
    if is_scripting():
        return False
    return torch._C._is_tracing()
