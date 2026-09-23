    def _tidy_repr(self, max_vals=20):
        """

        Internal function, should always return unicode string
        """
        num = max_vals // 2
        head = self.iloc[:num]._get_repr(print_header=True, length=False,
                                         dtype=False, name=False)
        tail = self.iloc[-(max_vals - num):]._get_repr(print_header=False,
                                                       length=False,
                                                       name=False,
                                                       dtype=False)
        result = head + '\n...\n' + tail
        result = '%s\n%s' % (result, self._repr_footer())

        return compat.text_type(result)
