    def _tidy_repr(self, max_vals=10, footer=True):
        """ a short repr displaying only max_vals and an optional (but default
        footer)
        """
        num = max_vals // 2
        head = self[:num]._get_repr(length=False, footer=False)
        tail = self[-(max_vals - num):]._get_repr(length=False, footer=False)

        result = u('{head}, ..., {tail}').format(head=head[:-1], tail=tail[1:])
        if footer:
            result = u('{result}\n{footer}').format(result=result,
                                                    footer=self._repr_footer())

        return compat.text_type(result)
