    def _evaluate_compare(self, other, op):
        """
        We have been called because a comparison between
        8 aware arrays. numpy >= 1.11 will
        now warn about NaT comparisons
        """

        # coerce to a similar object
        if not isinstance(other, type(self)):
            if not is_list_like(other):
                # scalar
                other = [other]
            elif is_scalar(lib.item_from_zerodim(other)):
                # ndarray scalar
                other = [other.item()]
            other = type(self)(other)

        # compare
        result = op(self.asi8, other.asi8)

        # technically we could support bool dtyped Index
        # for now just return the indexing array directly
        mask = (self._isnan) | (other._isnan)
        if is_bool_dtype(result):
            result[mask] = False
            return result
        try:
            result[mask] = iNaT
            return Index(result)
        except TypeError:
            return result
