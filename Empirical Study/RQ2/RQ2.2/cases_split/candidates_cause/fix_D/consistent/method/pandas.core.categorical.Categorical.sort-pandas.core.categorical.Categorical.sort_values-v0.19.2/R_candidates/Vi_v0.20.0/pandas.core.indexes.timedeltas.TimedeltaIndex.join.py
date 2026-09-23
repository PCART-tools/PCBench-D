    def join(self, other, how='left', level=None, return_indexers=False):
        """
        See Index.join
        """
        if _is_convertible_to_index(other):
            try:
                other = TimedeltaIndex(other)
            except (TypeError, ValueError):
                pass

        return Index.join(self, other, how=how, level=level,
                          return_indexers=return_indexers)
