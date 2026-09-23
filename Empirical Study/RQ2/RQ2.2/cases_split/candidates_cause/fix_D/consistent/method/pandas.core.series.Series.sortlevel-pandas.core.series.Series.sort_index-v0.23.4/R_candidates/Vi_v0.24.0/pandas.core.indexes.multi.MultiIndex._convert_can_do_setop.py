    def _convert_can_do_setop(self, other):
        result_names = self.names

        if not hasattr(other, 'names'):
            if len(other) == 0:
                other = MultiIndex(levels=[[]] * self.nlevels,
                                   codes=[[]] * self.nlevels,
                                   verify_integrity=False)
            else:
                msg = 'other must be a MultiIndex or a list of tuples'
                try:
                    other = MultiIndex.from_tuples(other)
                except TypeError:
                    raise TypeError(msg)
        else:
            result_names = self.names if self.names == other.names else None
        return other, result_names
