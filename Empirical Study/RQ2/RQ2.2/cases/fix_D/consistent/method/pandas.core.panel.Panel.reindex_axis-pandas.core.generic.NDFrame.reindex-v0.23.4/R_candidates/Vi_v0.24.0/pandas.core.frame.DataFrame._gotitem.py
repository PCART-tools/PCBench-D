    def _gotitem(self,
                 key,           # type: Union[str, List[str]]
                 ndim,          # type: int
                 subset=None    # type: Union[Series, DataFrame, None]
                 ):
        # type: (...) -> Union[Series, DataFrame]
        """
        Sub-classes to define. Return a sliced object.

        Parameters
        ----------
        key : string / list of selections
        ndim : 1,2
            requested ndim of result
        subset : object, default None
            subset to act on
        """
        if subset is None:
            subset = self
        elif subset.ndim == 1:  # is Series
            return subset

        # TODO: _shallow_copy(subset)?
        return subset[key]
