    @cbook.deprecated("3.0")
    def strftime(self, dt, fmt=None):
        """
        Refer to documentation for :meth:`datetime.datetime.strftime`

        *fmt* is a :meth:`datetime.datetime.strftime` format string.

        Warning: For years before 1900, depending upon the current
        locale it is possible that the year displayed with %x might
        be incorrect. For years before 100, %y and %Y will yield
        zero-padded strings.
        """
        if fmt is None:
            fmt = self.fmt
        fmt = self.illegal_s.sub(r"\1", fmt)
        fmt = fmt.replace("%s", "s")
        if dt.year >= 1900:
            # Note: in python 3.3 this is okay for years >= 1000,
            # refer to http://bugs.python.org/issue1777412
            return cbook.unicode_safe(dt.strftime(fmt))

        return self.strftime_pre_1900(dt, fmt)
