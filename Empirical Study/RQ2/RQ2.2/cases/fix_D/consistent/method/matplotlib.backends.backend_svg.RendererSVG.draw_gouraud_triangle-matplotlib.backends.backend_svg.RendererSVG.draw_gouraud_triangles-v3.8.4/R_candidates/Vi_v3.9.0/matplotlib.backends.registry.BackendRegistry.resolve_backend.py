    def resolve_backend(self, backend):
        """
        Return the backend and GUI framework for the specified backend name.

        If the GUI framework is not yet known then it will be determined by loading the
        backend module and checking the ``FigureCanvas.required_interactive_framework``
        attribute.

        This function only loads entry points if they have not already been loaded and
        the backend is not built-in and not of ``module://some.backend`` format.

        Parameters
        ----------
        backend : str or None
            Name of backend, or None to use the default backend.

        Returns
        -------
        backend : str
            The backend name.
        framework : str or None
            The GUI framework, which will be None for a backend that is non-interactive.
        """
        if isinstance(backend, str):
            backend = backend.lower()
        else:  # Might be _auto_backend_sentinel or None
            # Use whatever is already running...
            from matplotlib import get_backend
            backend = get_backend()

        # Is backend already known (built-in or dynamically loaded)?
        gui = (self._BUILTIN_BACKEND_TO_GUI_FRAMEWORK.get(backend) or
               self._backend_to_gui_framework.get(backend))

        # Is backend "module://something"?
        if gui is None and isinstance(backend, str) and backend.startswith("module://"):
            gui = "unknown"

        # Is backend a possible entry point?
        if gui is None and not self._loaded_entry_points:
            self._ensure_entry_points_loaded()
            gui = self._backend_to_gui_framework.get(backend)

        # Backend known but not its gui framework.
        if gui == "unknown":
            gui = self._get_gui_framework_by_loading(backend)
            self._backend_to_gui_framework[backend] = gui

        if gui is None:
            raise RuntimeError(f"'{backend}' is not a recognised backend name")

        return backend, gui if gui != "headless" else None
