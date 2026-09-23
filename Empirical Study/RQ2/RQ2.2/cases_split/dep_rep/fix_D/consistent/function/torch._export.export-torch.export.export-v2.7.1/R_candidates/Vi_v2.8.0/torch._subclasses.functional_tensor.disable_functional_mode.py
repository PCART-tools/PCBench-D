@contextlib.contextmanager
def disable_functional_mode():
    return _disable_infra_mode(torch._C._TorchDispatchModeKey.FUNCTIONAL)
