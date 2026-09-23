    def _set_name(
        self, name, inplace: bool = False, deep: bool | None = None
    ) -> Series:
        """
        Set the Series name.

        Parameters
        ----------
        name : str
        inplace : bool
            Whether to modify `self` directly or return a copy.
        deep : bool|None, default None
            Whether to do a deep copy, a shallow copy, or Copy on Write(None)
        """
        inplace = validate_bool_kwarg(inplace, "inplace")
        ser = self if inplace else self.copy(deep and not using_copy_on_write())
        ser.name = name
        return ser
