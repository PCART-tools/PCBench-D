    def filter(self, items=None, like=None, regex=None, axis=None):
        """
        Restrict the info axis to set of items or wildcard

        Parameters
        ----------
        items : list-like
            List of info axis to restrict to (must not all be present)
        like : string
            Keep info axis where "arg in col == True"
        regex : string (regular expression)
            Keep info axis with re.search(regex, col) == True
        axis : int or None
            The axis to filter on. By default this is the info axis. The "info
            axis" is the axis that is used when indexing with ``[]``. For
            example, ``df = DataFrame({'a': [1, 2, 3, 4]]}); df['a']``. So,
            the ``DataFrame`` columns are the info axis.

        Notes
        -----
        Arguments are mutually exclusive, but this is not checked for

        """
        import re

        if axis is None:
            axis = self._info_axis_name
        axis_name = self._get_axis_name(axis)
        axis_values = self._get_axis(axis_name)

        if items is not None:
            return self.reindex(**{axis_name: [r for r in items
                                               if r in axis_values]})
        elif like:
            matchf = lambda x: (like in x if isinstance(x, string_types)
                                else like in str(x))
            return self.select(matchf, axis=axis_name)
        elif regex:
            matcher = re.compile(regex)
            return self.select(lambda x: matcher.search(x) is not None,
                               axis=axis_name)
        else:
            raise TypeError('Must pass either `items`, `like`, or `regex`')
