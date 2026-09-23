    def _local_dir(self):
        """ add the string-like attributes from the info_axis """
        return [c for c in self._info_axis
                if isinstance(c, string_types) and isidentifier(c)]
