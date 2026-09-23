    def is_valid_backend(self, backend):
        """
        Return True if the backend name is valid, False otherwise.

        A backend name is valid if it is one of the built-in backends or has been
        dynamically added via an entry point. Those beginning with ``module://`` are
        always considered valid and are added to the current list of all backends
        within this function.

        Even if a name is valid, it may not be importable or usable. This can only be
        determined by loading and using the backend module.

        Parameters
        ----------
        backend : str
            Name of backend.

        Returns
        -------
        bool
            True if backend is valid, False otherwise.
        """
        if not backend.startswith("module://"):
            backend = backend.lower()

        # For backward compatibility, convert ipympl and matplotlib-inline long
        # module:// names to their shortened forms.
        backwards_compat = {
            "module://ipympl.backend_nbagg": "widget",
            "module://matplotlib_inline.backend_inline": "inline",
        }
        backend = backwards_compat.get(backend, backend)

        if (backend in self._BUILTIN_BACKEND_TO_GUI_FRAMEWORK or
                backend in self._backend_to_gui_framework):
            return True

        if backend.startswith("module://"):
            self._backend_to_gui_framework[backend] = "unknown"
            return True

        # Only load entry points if really need to and not already done so.
        self._ensure_entry_points_loaded()
        if backend in self._backend_to_gui_framework:
            return True

        return False
