@contextlib.contextmanager
def _enable(compiler_fn, dynamic=False):
    if dynamic:
        assert type(dynamic) is bool

    from torch._dynamo import eval_frame

    if eval_frame._stance.stance == "force_eager":
        # If user explicitly sets Dynamo stance to "force_eager", we want Compiled Autograd
        # to fall back to eager as well.
        global compiled_autograd_enabled_force_eager
        compiled_autograd_enabled_force_eager = True
        try:
            yield
        finally:
            compiled_autograd_enabled_force_eager = False
    else:
        # we need to import this, because user might not have imported it if they directly use this context manager
        # we need to lazily import it, because of circular dependencies
        import torch._inductor.cudagraph_trees

        (
            prior_compiler,
            prior_dynamic,
        ) = torch._C._dynamo.compiled_autograd.set_autograd_compiler(
            functools.partial(AutogradCompilerInstance, compiler_fn), dynamic
        )
        if snapshot_verbose_logging_enabled():
            torch._C._dynamo.compiled_autograd.set_verbose_logger(verbose_log)
        global compiled_autograd_enabled
        compiled_autograd_enabled = True
        try:
            with torch.autograd.set_multithreading_enabled(False):
                yield
        finally:
            if not prior_compiler:
                compiled_autograd_enabled = False
            torch._C._dynamo.compiled_autograd.set_autograd_compiler(
                prior_compiler, prior_dynamic
            )
