    def _check_is_chained_assignment_possible(self):
        """
        check if we are a view, have a cacher, and are of mixed type
        if so, then force a setitem_copy check

        should be called just near setting a value

        will return a boolean if it we are a view and are cached, but a single-dtype
        meaning that the cacher should be updated following setting
        """
        if self._is_view and self._is_cached:
            ref = self._get_cacher()
            if ref is not None and ref._is_mixed_type:
                self._check_setitem_copy(stacklevel=4, t='referant', force=True)
            return True
        elif self.is_copy:
            self._check_setitem_copy(stacklevel=4, t='referant')
        return False
