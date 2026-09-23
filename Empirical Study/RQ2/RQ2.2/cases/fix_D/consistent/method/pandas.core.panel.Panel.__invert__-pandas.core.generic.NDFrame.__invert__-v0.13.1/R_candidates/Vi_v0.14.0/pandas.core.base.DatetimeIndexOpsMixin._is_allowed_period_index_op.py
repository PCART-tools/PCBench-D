    def _is_allowed_period_index_op(self, name):
        if not self._allow_period_index_ops:
            raise TypeError("cannot perform an {name} operations on this type {typ}".format(
                name=name,typ=type(self._get_access_object())))
