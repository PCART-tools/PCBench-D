    def backend_for_gui_framework(self, framework):
        """
        Return the name of the backend corresponding to the specified GUI framework.

        Parameters
        ----------
        framework : str
            GUI framework such as "qt".

        Returns
        -------
        str or None
            Backend name or None if GUI framework not recognised.
        """
        return self._GUI_FRAMEWORK_TO_BACKEND.get(framework.lower())
