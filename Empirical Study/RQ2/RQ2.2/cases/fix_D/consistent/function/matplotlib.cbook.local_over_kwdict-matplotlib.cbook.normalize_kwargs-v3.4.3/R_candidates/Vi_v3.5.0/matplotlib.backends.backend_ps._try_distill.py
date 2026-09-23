def _try_distill(func, *args, **kwargs):
    try:
        func(*args, **kwargs)
    except mpl.ExecutableNotFoundError as exc:
        _log.warning("%s.  Distillation step skipped.", exc)
