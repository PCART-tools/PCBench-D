def warn_external(message, category=None):
    """
    `warnings.warn` wrapper that sets *stacklevel* to "outside Matplotlib".

    The original emitter of the warning can be obtained by patching this
    function back to `warnings.warn`, i.e. ``_api.warn_external =
    warnings.warn`` (or ``functools.partial(warnings.warn, stacklevel=2)``,
    etc.).
    """
    frame = sys._getframe()
    for stacklevel in itertools.count(1):  # lgtm[py/unused-loop-variable]
        if frame is None:
            # when called in embedded context may hit frame is None
            break
        if not re.match(r"\A(matplotlib|mpl_toolkits)(\Z|\.(?!tests\.))",
                        # Work around sphinx-gallery not setting __name__.
                        frame.f_globals.get("__name__", "")):
            break
        frame = frame.f_back
    warnings.warn(message, category, stacklevel)
