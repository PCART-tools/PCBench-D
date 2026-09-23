    def update(self, other, join='left', overwrite=True, filter_func=None,
               raise_conflict=False):
        """
        Modify DataFrame in place using non-NA values from passed
        DataFrame. Aligns on indices

        Parameters
        ----------
        other : DataFrame, or object coercible into a DataFrame
        join : {'left'}, default 'left'
        overwrite : boolean, default True
            If True then overwrite values for common keys in the calling frame
        filter_func : callable(1d-array) -> 1d-array<boolean>, default None
            Can choose to replace values other than NA. Return True for values
            that should be updated
        raise_conflict : boolean
            If True, will raise an error if the DataFrame and other both
            contain data in the same place.
        """
        # TODO: Support other joins
        if join != 'left':  # pragma: no cover
            raise NotImplementedError("Only left join is supported")

        if not isinstance(other, DataFrame):
            other = DataFrame(other)

        other = other.reindex_like(self)

        for col in self.columns:
            this = self[col].values
            that = other[col].values
            if filter_func is not None:
                mask = ~filter_func(this) | isnull(that)
            else:
                if raise_conflict:
                    mask_this = notnull(that)
                    mask_that = notnull(this)
                    if any(mask_this & mask_that):
                        raise ValueError("Data overlaps.")

                if overwrite:
                    mask = isnull(that)

                    # don't overwrite columns unecessarily
                    if mask.all():
                        continue
                else:
                    mask = notnull(this)

            self[col] = expressions.where(
                mask, this, that, raise_on_error=True)
