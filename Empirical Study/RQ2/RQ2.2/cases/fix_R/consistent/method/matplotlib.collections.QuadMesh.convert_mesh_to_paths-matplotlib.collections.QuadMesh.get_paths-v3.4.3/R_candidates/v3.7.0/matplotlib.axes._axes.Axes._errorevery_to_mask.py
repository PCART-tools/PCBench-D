    @staticmethod
    def _errorevery_to_mask(x, errorevery):
        """
        Normalize `errorbar`'s *errorevery* to be a boolean mask for data *x*.

        This function is split out to be usable both by 2D and 3D errorbars.
        """
        if isinstance(errorevery, Integral):
            errorevery = (0, errorevery)
        if isinstance(errorevery, tuple):
            if (len(errorevery) == 2 and
                    isinstance(errorevery[0], Integral) and
                    isinstance(errorevery[1], Integral)):
                errorevery = slice(errorevery[0], None, errorevery[1])
            else:
                raise ValueError(
                    f'{errorevery=!r} is a not a tuple of two integers')
        elif isinstance(errorevery, slice):
            pass
        elif not isinstance(errorevery, str) and np.iterable(errorevery):
            try:
                x[errorevery]  # fancy indexing
            except (ValueError, IndexError) as err:
                raise ValueError(
                    f"{errorevery=!r} is iterable but not a valid NumPy fancy "
                    "index to match 'xerr'/'yerr'") from err
        else:
            raise ValueError(f"{errorevery=!r} is not a recognized value")
        everymask = np.zeros(len(x), bool)
        everymask[errorevery] = True
        return everymask
