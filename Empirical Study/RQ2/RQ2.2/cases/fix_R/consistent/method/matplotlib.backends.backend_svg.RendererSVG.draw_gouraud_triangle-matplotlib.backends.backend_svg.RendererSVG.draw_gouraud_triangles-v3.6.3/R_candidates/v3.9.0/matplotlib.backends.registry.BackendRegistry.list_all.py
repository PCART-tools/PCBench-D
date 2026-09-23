    def list_all(self):
        """
        Return list of all known backends.

        These include built-in backends and those obtained at runtime either from entry
        points or explicit ``module://some.backend`` syntax.

        Entry points will be loaded if they haven't been already.

        Returns
        -------
        list of str
            Backend names.
        """
        self._ensure_entry_points_loaded()
        return [*self.list_builtin(), *self._backend_to_gui_framework]
