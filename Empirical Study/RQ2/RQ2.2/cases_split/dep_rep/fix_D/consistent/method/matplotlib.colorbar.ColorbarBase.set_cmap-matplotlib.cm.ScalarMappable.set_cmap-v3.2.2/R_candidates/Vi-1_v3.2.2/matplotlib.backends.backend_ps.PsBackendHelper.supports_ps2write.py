    @cbook.deprecated("3.1")
    @property
    def supports_ps2write(self):
        """
        True if the installed ghostscript supports ps2write device.
        """
        return self.gs_version[0] >= 9
