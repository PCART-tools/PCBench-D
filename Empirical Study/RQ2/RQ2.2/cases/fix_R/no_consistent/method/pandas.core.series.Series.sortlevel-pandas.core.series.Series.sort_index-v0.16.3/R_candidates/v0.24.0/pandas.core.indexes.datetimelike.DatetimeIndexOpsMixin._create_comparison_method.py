    @classmethod
    def _create_comparison_method(cls, op):
        """
        Create a comparison method that dispatches to ``cls.values``.
        """
        def wrapper(self, other):
            if isinstance(other, ABCSeries):
                # the arrays defer to Series for comparison ops but the indexes
                #  don't, so we have to unwrap here.
                other = other._values

            result = op(self._data, maybe_unwrap_index(other))
            return result

        wrapper.__doc__ = op.__doc__
        wrapper.__name__ = '__{}__'.format(op.__name__)
        return wrapper
