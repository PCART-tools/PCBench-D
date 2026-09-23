    @final
    def _union_incompatible_dtypes(self, other, sort):
        """
        Casts this and other index to object dtype to allow the formation
        of a union between incompatible types.

        Parameters
        ----------
        other : Index or array-like
        sort : False or None, default False
            Whether to sort the resulting index.

            * False : do not sort the result.
            * None : sort the result, except when `self` and `other` are equal
              or when the values cannot be compared.

        Returns
        -------
        Index
        """
        this = self.astype(object, copy=False)
        # cast to Index for when `other` is list-like
        other = Index(other).astype(object, copy=False)
        return Index.union(this, other, sort=sort).astype(object, copy=False)
