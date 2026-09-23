    def _set_formatter(self, formatter, level):
        if isinstance(formatter, str):
            formatter = mticker.StrMethodFormatter(formatter)
        # Don't allow any other TickHelper to avoid easy-to-make errors,
        # like using a Locator instead of a Formatter.
        elif (callable(formatter) and
              not isinstance(formatter, mticker.TickHelper)):
            formatter = mticker.FuncFormatter(formatter)
        else:
            _api.check_isinstance(mticker.Formatter, formatter=formatter)

        if (isinstance(formatter, mticker.FixedFormatter)
                and len(formatter.seq) > 0
                and not isinstance(level.locator, mticker.FixedLocator)):
            _api.warn_external('FixedFormatter should only be used together '
                               'with FixedLocator')

        if level == self.major:
            self.isDefault_majfmt = False
        else:
            self.isDefault_minfmt = False

        level.formatter = formatter
        formatter.set_axis(self)
        self.stale = True
