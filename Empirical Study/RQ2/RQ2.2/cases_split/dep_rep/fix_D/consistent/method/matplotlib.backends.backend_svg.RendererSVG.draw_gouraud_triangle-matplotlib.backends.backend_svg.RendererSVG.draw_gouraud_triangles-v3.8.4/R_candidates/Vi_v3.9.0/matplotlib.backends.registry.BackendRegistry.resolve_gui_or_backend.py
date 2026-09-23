    def resolve_gui_or_backend(self, gui_or_backend):
        """
        Return the backend and GUI framework for the specified string that may be
        either a GUI framework or a backend name, tested in that order.

        This is for use with the IPython %matplotlib magic command which may be a GUI
        framework such as ``%matplotlib qt`` or a backend name such as
        ``%matplotlib qtagg``.

        This function only loads entry points if they have not already been loaded and
        the backend is not built-in and not of ``module://some.backend`` format.

        Parameters
        ----------
        gui_or_backend : str or None
            Name of GUI framework or backend, or None to use the default backend.

        Returns
        -------
        backend : str
            The backend name.
        framework : str or None
            The GUI framework, which will be None for a backend that is non-interactive.
        """
        gui_or_backend = gui_or_backend.lower()

        # First check if it is a gui loop name.
        backend = self.backend_for_gui_framework(gui_or_backend)
        if backend is not None:
            return backend, gui_or_backend if gui_or_backend != "headless" else None

        # Then check if it is a backend name.
        try:
            return self.resolve_backend(gui_or_backend)
        except Exception:  # KeyError ?
            raise RuntimeError(
                f"'{gui_or_backend} is not a recognised GUI loop or backend name")
