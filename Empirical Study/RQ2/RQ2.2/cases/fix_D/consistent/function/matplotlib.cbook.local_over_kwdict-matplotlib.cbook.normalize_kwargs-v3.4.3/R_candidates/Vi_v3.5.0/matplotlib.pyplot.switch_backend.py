def switch_backend(newbackend):
    """
    Close all open figures and set the Matplotlib backend.

    The argument is case-insensitive.  Switching to an interactive backend is
    possible only if no event loop for another interactive backend has started.
    Switching to and from non-interactive backends is always possible.

    Parameters
    ----------
    newbackend : str
        The name of the backend to use.
    """
    global _backend_mod
    # make sure the init is pulled up so we can assign to it later
    import matplotlib.backends
    close("all")

    if newbackend is rcsetup._auto_backend_sentinel:
        current_framework = cbook._get_running_interactive_framework()
        mapping = {'qt': 'qtagg',
                   'gtk3': 'gtk3agg',
                   'gtk4': 'gtk4agg',
                   'wx': 'wxagg',
                   'tk': 'tkagg',
                   'macosx': 'macosx',
                   'headless': 'agg'}

        best_guess = mapping.get(current_framework, None)
        if best_guess is not None:
            candidates = [best_guess]
        else:
            candidates = []
        candidates += [
            "macosx", "qtagg", "gtk4agg", "gtk3agg", "tkagg", "wxagg"]

        # Don't try to fallback on the cairo-based backends as they each have
        # an additional dependency (pycairo) over the agg-based backend, and
        # are of worse quality.
        for candidate in candidates:
            try:
                switch_backend(candidate)
            except ImportError:
                continue
            else:
                rcParamsOrig['backend'] = candidate
                return
        else:
            # Switching to Agg should always succeed; if it doesn't, let the
            # exception propagate out.
            switch_backend("agg")
            rcParamsOrig["backend"] = "agg"
            return

    # Backends are implemented as modules, but "inherit" default method
    # implementations from backend_bases._Backend.  This is achieved by
    # creating a "class" that inherits from backend_bases._Backend and whose
    # body is filled with the module's globals.

    backend_name = cbook._backend_module_name(newbackend)

    class backend_mod(matplotlib.backend_bases._Backend):
        locals().update(vars(importlib.import_module(backend_name)))

    required_framework = _get_required_interactive_framework(backend_mod)
    if required_framework is not None:
        current_framework = cbook._get_running_interactive_framework()
        if (current_framework and required_framework
                and current_framework != required_framework):
            raise ImportError(
                "Cannot load backend {!r} which requires the {!r} interactive "
                "framework, as {!r} is currently running".format(
                    newbackend, required_framework, current_framework))

    _log.debug("Loaded backend %s version %s.",
               newbackend, backend_mod.backend_version)

    rcParams['backend'] = rcParamsDefault['backend'] = newbackend
    _backend_mod = backend_mod
    for func_name in ["new_figure_manager", "draw_if_interactive", "show"]:
        globals()[func_name].__signature__ = inspect.signature(
            getattr(backend_mod, func_name))

    # Need to keep a global reference to the backend for compatibility reasons.
    # See https://github.com/matplotlib/matplotlib/issues/6092
    matplotlib.backends.backend = newbackend
