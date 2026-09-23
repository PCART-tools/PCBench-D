    @property
    def gs_version(self):
        """
        version of ghostscript.
        """
        try:
            return self._cached["gs_version"]
        except KeyError:
            pass

        s = subprocess.Popen(
            [self.gs_exe, "--version"], stdout=subprocess.PIPE)
        pipe, stderr = s.communicate()
        ver = pipe.decode('ascii')
        try:
            gs_version = tuple(map(int, ver.strip().split(".")))
        except ValueError:
            # if something went wrong parsing return null version number
            gs_version = (0, 0)
        self._cached["gs_version"] = gs_version
        return gs_version
