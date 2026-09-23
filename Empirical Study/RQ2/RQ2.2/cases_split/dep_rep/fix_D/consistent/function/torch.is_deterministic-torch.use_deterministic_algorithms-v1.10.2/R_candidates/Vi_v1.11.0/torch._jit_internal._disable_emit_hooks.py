@contextlib.contextmanager
def _disable_emit_hooks():
    hooks = torch._C._jit_get_emit_hooks()
    torch._C._jit_set_emit_hooks(None, None)
    yield
    torch._C._jit_set_emit_hooks(hooks[0], hooks[1])
