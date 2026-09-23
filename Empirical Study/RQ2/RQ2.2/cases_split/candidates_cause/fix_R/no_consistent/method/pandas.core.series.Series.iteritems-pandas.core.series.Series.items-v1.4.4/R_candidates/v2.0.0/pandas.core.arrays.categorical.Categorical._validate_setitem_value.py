    def _validate_setitem_value(self, value):
        if not is_hashable(value):
            # wrap scalars and hashable-listlikes in list
            return self._validate_listlike(value)
        else:
            return self._validate_scalar(value)
