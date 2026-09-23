    def list_builtin(self, filter_=None):
        """
        Return list of backends that are built into Matplotlib.

        Parameters
        ----------
        filter_ : `~.BackendFilter`, optional
            Filter to apply to returned backends. For example, to return only
            non-interactive backends use `.BackendFilter.NON_INTERACTIVE`.

        Returns
        -------
        list of str
            Backend names.
        """
        if filter_ == BackendFilter.INTERACTIVE:
            return [k for k, v in self._BUILTIN_BACKEND_TO_GUI_FRAMEWORK.items()
                    if v != "headless"]
        elif filter_ == BackendFilter.NON_INTERACTIVE:
            return [k for k, v in self._BUILTIN_BACKEND_TO_GUI_FRAMEWORK.items()
                    if v == "headless"]

        return [*self._BUILTIN_BACKEND_TO_GUI_FRAMEWORK]
