    @final
    def _get_numeric_data(self) -> Self:
        new_mgr = self._mgr.get_numeric_data()
        return self._constructor_from_mgr(new_mgr, axes=new_mgr.axes).__finalize__(self)
