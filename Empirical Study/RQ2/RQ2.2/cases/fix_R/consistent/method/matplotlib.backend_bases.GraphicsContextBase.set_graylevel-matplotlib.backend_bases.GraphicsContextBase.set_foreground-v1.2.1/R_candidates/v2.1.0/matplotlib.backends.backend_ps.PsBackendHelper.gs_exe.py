    @property
    def gs_exe(self):
        """
        excutable name of ghostscript.
        """
        try:
            return self._cached["gs_exe"]
        except KeyError:
            pass

        gs_exe, gs_version = checkdep_ghostscript()
        if gs_exe is None:
            gs_exe = 'gs'

        self._cached["gs_exe"] = str(gs_exe)
        return str(gs_exe)
