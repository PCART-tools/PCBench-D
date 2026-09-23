    def list_gui_frameworks(self):
        """
        Return list of GUI frameworks used by Matplotlib backends.

        Returns
        -------
        list of str
            GUI framework names.
        """
        return [k for k in self._GUI_FRAMEWORK_TO_BACKEND if k != "headless"]
