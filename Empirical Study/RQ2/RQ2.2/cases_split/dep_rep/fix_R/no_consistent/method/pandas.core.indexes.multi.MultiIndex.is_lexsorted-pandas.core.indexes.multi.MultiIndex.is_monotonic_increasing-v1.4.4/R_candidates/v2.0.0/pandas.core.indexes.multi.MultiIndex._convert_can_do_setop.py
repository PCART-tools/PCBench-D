    def _convert_can_do_setop(self, other):
        result_names = self.names

        if not isinstance(other, Index):
            if len(other) == 0:
                return self[:0], self.names
            else:
                msg = "other must be a MultiIndex or a list of tuples"
                try:
                    other = MultiIndex.from_tuples(other, names=self.names)
                except (ValueError, TypeError) as err:
                    # ValueError raised by tuples_to_object_array if we
                    #  have non-object dtype
                    raise TypeError(msg) from err
        else:
            result_names = get_unanimous_names(self, other)

        return other, result_names
