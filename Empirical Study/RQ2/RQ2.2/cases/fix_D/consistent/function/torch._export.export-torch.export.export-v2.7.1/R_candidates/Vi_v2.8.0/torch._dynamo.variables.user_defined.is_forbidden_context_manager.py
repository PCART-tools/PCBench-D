def is_forbidden_context_manager(ctx):
    f_ctxs = []

    try:
        from _pytest.python_api import RaisesContext
        from _pytest.recwarn import WarningsChecker

        f_ctxs.append(RaisesContext)
        f_ctxs.append(WarningsChecker)
    except ImportError:
        pass

    if m := sys.modules.get("torch.testing._internal.jit_utils"):
        f_ctxs.append(m._AssertRaisesRegexWithHighlightContext)

    return ctx in f_ctxs
