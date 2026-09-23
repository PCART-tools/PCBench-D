    def set_fontconfig_pattern(self, pattern):
        """
        Set the properties by parsing a fontconfig *pattern*.

        See the documentation on `fontconfig patterns
        <https://www.freedesktop.org/software/fontconfig/fontconfig-user.html>`_.

        This support does not require fontconfig to be installed or
        support for it to be enabled.  We are merely borrowing its
        pattern syntax for use here.
        """
        for key, val in six.iteritems(self._parse_fontconfig_pattern(pattern)):
            if type(val) == list:
                getattr(self, "set_" + key)(val[0])
            else:
                getattr(self, "set_" + key)(val)
