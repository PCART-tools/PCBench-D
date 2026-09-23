    def _expand_ellipsis(self, tup: tuple) -> tuple:
        """
        If a tuple key includes an Ellipsis, replace it with an appropriate
        number of null slices.
        """
        if any(x is Ellipsis for x in tup):
            if tup.count(Ellipsis) > 1:
                raise IndexingError(_one_ellipsis_message)

            if len(tup) == self.ndim:
                # It is unambiguous what axis this Ellipsis is indexing,
                #  treat as a single null slice.
                i = tup.index(Ellipsis)
                # FIXME: this assumes only one Ellipsis
                new_key = tup[:i] + (_NS,) + tup[i + 1 :]
                return new_key

            # TODO: other cases?  only one test gets here, and that is covered
            #  by _validate_key_length
        return tup
