    def _tidy_repr(self, max_vals=20):
        num = max_vals // 2
        head = self[:num]._get_repr(length=False, name=False, footer=False)
        tail = self[-(max_vals - num):]._get_repr(length=False,
                                                  name=False,
                                                  footer=False)

        result = '%s\n...\n%s' % (head, tail)
        # TODO: tidy_repr for footer since there may be a ton of levels?
        result = '%s\n%s' % (result, self._repr_footer())

        return compat.text_type(result)
