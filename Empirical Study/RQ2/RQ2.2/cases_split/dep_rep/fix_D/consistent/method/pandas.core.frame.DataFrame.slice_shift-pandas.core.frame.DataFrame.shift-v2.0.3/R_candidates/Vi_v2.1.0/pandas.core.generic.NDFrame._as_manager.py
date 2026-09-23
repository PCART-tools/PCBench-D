    @final
    def _as_manager(self, typ: str, copy: bool_t = True) -> Self:
        """
        Private helper function to create a DataFrame with specific manager.

        Parameters
        ----------
        typ : {"block", "array"}
        copy : bool, default True
            Only controls whether the conversion from Block->ArrayManager
            copies the 1D arrays (to ensure proper/contiguous memory layout).

        Returns
        -------
        DataFrame
            New DataFrame using specified manager type. Is not guaranteed
            to be a copy or not.
        """
        new_mgr: Manager
        new_mgr = mgr_to_mgr(self._mgr, typ=typ, copy=copy)
        # fastpath of passing a manager doesn't check the option/manager class
        return self._constructor_from_mgr(new_mgr, axes=new_mgr.axes).__finalize__(self)
