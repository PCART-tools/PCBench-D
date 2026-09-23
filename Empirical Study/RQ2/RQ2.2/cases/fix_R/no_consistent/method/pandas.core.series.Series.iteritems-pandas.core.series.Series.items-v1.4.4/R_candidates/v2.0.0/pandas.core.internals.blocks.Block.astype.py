    @final
    def astype(
        self,
        dtype: DtypeObj,
        copy: bool = False,
        errors: IgnoreRaise = "raise",
        using_cow: bool = False,
    ) -> Block:
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
        using_cow: bool, default False
            Signaling if copy on write copy logic is used.

        Returns
        -------
        Block
        """
        values = self.values

        new_values = astype_array_safe(values, dtype, copy=copy, errors=errors)

        new_values = maybe_coerce_values(new_values)

        refs = None
        if using_cow and astype_is_view(values.dtype, new_values.dtype):
            refs = self.refs

        newb = self.make_block(new_values, refs=refs)
        if newb.shape != self.shape:
            raise TypeError(
                f"cannot set astype for copy = [{copy}] for dtype "
                f"({self.dtype.name} [{self.shape}]) to different shape "
                f"({newb.dtype.name} [{newb.shape}])"
            )
        return newb
