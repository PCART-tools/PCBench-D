class PsBackendHelper(object):

    def __init__(self):
        self._cached = {}

    @property
    def gs_exe(self):
        """
        executable name of ghostscript.
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

    @property
    def supports_ps2write(self):
        """
        True if the installed ghostscript supports ps2write device.
        """
        return self.gs_version[0] >= 9
