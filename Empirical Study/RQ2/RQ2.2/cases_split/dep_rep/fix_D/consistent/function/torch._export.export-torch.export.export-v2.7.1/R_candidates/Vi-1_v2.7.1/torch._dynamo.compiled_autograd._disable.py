@contextlib.contextmanager
def _disable():
    (
        prior_compiler,
        prior_dynamic,
    ) = torch._C._dynamo.compiled_autograd.set_autograd_compiler(None, False)
    global compiled_autograd_enabled
    compiled_autograd_enabled = False
    try:
        yield
    finally:
        if prior_compiler:
            compiled_autograd_enabled = True
        torch._C._dynamo.compiled_autograd.set_autograd_compiler(
            prior_compiler, prior_dynamic
        )
