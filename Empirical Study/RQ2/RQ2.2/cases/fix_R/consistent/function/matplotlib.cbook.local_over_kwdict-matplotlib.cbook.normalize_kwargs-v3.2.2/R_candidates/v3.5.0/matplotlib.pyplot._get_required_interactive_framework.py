def _get_required_interactive_framework(backend_mod):
    return getattr(
        backend_mod.FigureCanvas, "required_interactive_framework", None)
