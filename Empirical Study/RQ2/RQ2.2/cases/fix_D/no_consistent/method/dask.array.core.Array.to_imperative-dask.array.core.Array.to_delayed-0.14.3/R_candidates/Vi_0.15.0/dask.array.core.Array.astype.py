    def astype(self, dtype, **kwargs):
        """Copy of the array, cast to a specified type.

        Parameters
        ----------
        dtype : str or dtype
            Typecode or data-type to which the array is cast.
        casting : {'no', 'equiv', 'safe', 'same_kind', 'unsafe'}, optional
            Controls what kind of data casting may occur. Defaults to 'unsafe'
            for backwards compatibility.

            * 'no' means the data types should not be cast at all.
            * 'equiv' means only byte-order changes are allowed.
            * 'safe' means only casts which can preserve values are allowed.
            * 'same_kind' means only safe casts or casts within a kind,
                like float64 to float32, are allowed.
            * 'unsafe' means any data conversions may be done.
        copy : bool, optional
            By default, astype always returns a newly allocated array. If this
            is set to False and the `dtype` requirement is satisfied, the input
            array is returned instead of a copy.
        """
        # Scalars don't take `casting` or `copy` kwargs - as such we only pass
        # them to `map_blocks` if specified by user (different than defaults).
        extra = set(kwargs) - {'casting', 'copy'}
        if extra:
            raise TypeError("astype does not take the following keyword "
                            "arguments: {0!s}".format(list(extra)))
        casting = kwargs.get('casting', 'unsafe')
        copy = kwargs.get('copy', True)
        dtype = np.dtype(dtype)
        if self.dtype == dtype:
            return self
        elif not np.can_cast(self.dtype, dtype, casting=casting):
            raise TypeError("Cannot cast array from {0!r} to {1!r}"
                            " according to the rule "
                            "{2!r}".format(self.dtype, dtype, casting))
        name = 'astype-' + tokenize(self, dtype, casting, copy)
        return self.map_blocks(_astype, dtype=dtype, name=name,
                               astype_dtype=dtype, **kwargs)
