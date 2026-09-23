    def _ops_compat(self, name, op_accessor):

        obj = self._get_access_object()
        try:
            return self._wrap_access_object(getattr(obj,op_accessor))
        except AttributeError:
            raise TypeError("cannot perform an {name} operations on this type {typ}".format(
                name=name,typ=type(obj)))
