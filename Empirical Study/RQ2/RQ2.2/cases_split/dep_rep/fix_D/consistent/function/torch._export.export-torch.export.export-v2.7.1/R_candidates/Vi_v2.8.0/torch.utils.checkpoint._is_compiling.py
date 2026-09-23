def _is_compiling(func, args, kwargs):
    # Check if we are under AOTAutograd tracing
    # Checking that a functional mode is active should always do what we want
    return torch._C._get_dispatch_mode(torch._C._TorchDispatchModeKey.FUNCTIONAL) is not None
