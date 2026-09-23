    def _tidy_repr(self, max_vals=10):
        num = max_vals // 2
        head = self[:num]._get_repr(length=False, name=False, footer=False)
        tail = self[-(max_vals - num):]._get_repr(length=False,
                                                  name=False,
                                                  footer=False)

        result = '%s, ..., %s' % (head[:-1], tail[1:])
        result = '%s\n%s' % (result, self._repr_footer())

        return compat.text_type(result)
