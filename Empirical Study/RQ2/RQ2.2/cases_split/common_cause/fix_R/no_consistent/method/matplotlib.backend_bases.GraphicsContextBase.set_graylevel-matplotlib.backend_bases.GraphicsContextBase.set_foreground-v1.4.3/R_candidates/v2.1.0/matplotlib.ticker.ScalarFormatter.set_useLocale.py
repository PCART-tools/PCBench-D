    def set_useLocale(self, val):
        if val is None:
            self._useLocale = rcParams['axes.formatter.use_locale']
        else:
            self._useLocale = val
