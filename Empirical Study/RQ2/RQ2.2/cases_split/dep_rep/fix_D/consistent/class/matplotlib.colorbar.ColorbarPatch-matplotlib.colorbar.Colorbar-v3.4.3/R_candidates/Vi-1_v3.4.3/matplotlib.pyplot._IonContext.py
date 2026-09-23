class _IonContext:
    """
    Context manager for `.ion`.

    The state is changed in ``__init__()`` instead of ``__enter__()``. The
    latter is a no-op. This allows using `.ion` both as a function and
    as a context.
    """

    def __init__(self):
        self.wasinteractive = isinteractive()
        matplotlib.interactive(True)
        install_repl_displayhook()

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        if not self.wasinteractive:
            matplotlib.interactive(False)
            uninstall_repl_displayhook()
        else:
            matplotlib.interactive(True)
            install_repl_displayhook()
