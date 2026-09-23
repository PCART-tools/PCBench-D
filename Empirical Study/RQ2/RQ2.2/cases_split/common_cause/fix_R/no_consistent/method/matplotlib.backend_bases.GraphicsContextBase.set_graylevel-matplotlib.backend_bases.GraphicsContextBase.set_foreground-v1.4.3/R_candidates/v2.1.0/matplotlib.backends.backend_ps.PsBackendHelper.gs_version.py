    @property
    def gs_version(self):
        """
        version of ghostscript.
        """
        try:
            return self._cached["gs_version"]
        except KeyError:
            pass

        from matplotlib.compat.subprocess import Popen, PIPE
        s = Popen([self.gs_exe, "--version"], stdout=PIPE)
        pipe, stderr = s.communicate()
        if six.PY3:
            ver = pipe.decode('ascii')
        else:
            ver = pipe
        try:
            gs_version = tuple(map(int, ver.strip().split(".")))
        except ValueError:
            # if something went wrong parsing return null version number
            gs_version = (0, 0)
        self._cached["gs_version"] = gs_version
        return gs_version
