    @final
    def _get_bool_data(self):
        new_mgr = self._mgr.get_bool_data()
        return self._constructor_from_mgr(new_mgr, axes=new_mgr.axes).__finalize__(self)
