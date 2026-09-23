    def parse(self, pattern):
        """
        Parse the given fontconfig *pattern* and return a dictionary
        of key/value pairs useful for initializing a
        `.font_manager.FontProperties` object.
        """
        props = self._properties = {}
        try:
            self._parser.parseString(pattern)
        except self.ParseException as e:
            raise ValueError(
                "Could not parse font string: '%s'\n%s" % (pattern, e)) from e

        self._properties = None

        self._parser.resetCache()

        return props
