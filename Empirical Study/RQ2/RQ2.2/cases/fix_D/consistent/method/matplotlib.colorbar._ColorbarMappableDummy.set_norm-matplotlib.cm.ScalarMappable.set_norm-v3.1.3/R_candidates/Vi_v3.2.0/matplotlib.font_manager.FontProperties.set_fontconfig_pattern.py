    def set_fontconfig_pattern(self, pattern):
        """
        Set the properties by parsing a fontconfig_ *pattern*.

        This support does not depend on fontconfig; we are merely borrowing its
        pattern syntax for use here.
        """
        for key, val in self._parse_fontconfig_pattern(pattern).items():
            if type(val) == list:
                getattr(self, "set_" + key)(val[0])
            else:
                getattr(self, "set_" + key)(val)
