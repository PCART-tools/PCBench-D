    @final
    def astype(self, dtype: DtypeObj, copy: bool = False, errors: str = "raise"):
        """
        Coerce to the new dtype.

        Parameters
        ----------
        dtype : np.dtype or ExtensionDtype
        copy : bool, default False
            copy if indicated
        errors : str, {'raise', 'ignore'}, default 'raise'
            - ``raise`` : allow exceptions to be raised
            - ``ignore`` : suppress exceptions. On error return original object

        Returns
        -------
        Block
        """
        values = self.values

        new_values = astype_array_safe(values, dtype, copy=copy, errors=errors)

        new_values = maybe_coerce_values(new_values)
        newb = self.make_block(new_values)
        if newb.shape != self.shape:
            raise TypeError(
                f"cannot set astype for copy = [{copy}] for dtype "
                f"({self.dtype.name} [{self.shape}]) to different shape "
                f"({newb.dtype.name} [{newb.shape}])"
            )
        return newb
