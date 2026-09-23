    def set_level(self, level):
        'set the verbosity to one of the Verbose.levels strings'

        if self._commandLineVerbose is not None:
            level = self._commandLineVerbose
        if level not in self.levels:
            warnings.warn('matplotlib: unrecognized --verbose-* string "%s".'
                          ' Legal values are %s' % (level, self.levels))
        else:
            self.level = level
