    def join(self, other, how='left', level=None, return_indexers=False,
             sort=False):
        """
        See Index.join
        """
        if (not isinstance(other, DatetimeIndex) and len(other) > 0 and
            other.inferred_type not in ('floating', 'integer', 'mixed-integer',
                                        'mixed-integer-float', 'mixed')):
            try:
                other = DatetimeIndex(other)
            except (TypeError, ValueError):
                pass

        this, other = self._maybe_utc_convert(other)
        return Index.join(this, other, how=how, level=level,
                          return_indexers=return_indexers, sort=sort)
