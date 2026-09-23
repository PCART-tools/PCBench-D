    def _check_is_chained_assignment_possible(self) -> bool_t:
        """
        Check if we are a view, have a cacher, and are of mixed type.
        If so, then force a setitem_copy check.

        Should be called just near setting a value

        Will return a boolean if it we are a view and are cached, but a
        single-dtype meaning that the cacher should be updated following
        setting.
        """
        if self._is_copy:
            self._check_setitem_copy(t="referent")
        return False
