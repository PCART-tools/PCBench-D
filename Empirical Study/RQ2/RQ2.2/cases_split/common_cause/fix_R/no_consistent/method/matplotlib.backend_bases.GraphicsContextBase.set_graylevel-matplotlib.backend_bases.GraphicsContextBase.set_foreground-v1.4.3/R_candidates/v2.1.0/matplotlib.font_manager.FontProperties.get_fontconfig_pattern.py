    def get_fontconfig_pattern(self):
        """
        Get a fontconfig pattern suitable for looking up the font as
        specified with fontconfig's ``fc-match`` utility.

        See the documentation on `fontconfig patterns
        <https://www.freedesktop.org/software/fontconfig/fontconfig-user.html>`_.

        This support does not require fontconfig to be installed or
        support for it to be enabled.  We are merely borrowing its
        pattern syntax for use here.
        """
        return generate_fontconfig_pattern(self)
