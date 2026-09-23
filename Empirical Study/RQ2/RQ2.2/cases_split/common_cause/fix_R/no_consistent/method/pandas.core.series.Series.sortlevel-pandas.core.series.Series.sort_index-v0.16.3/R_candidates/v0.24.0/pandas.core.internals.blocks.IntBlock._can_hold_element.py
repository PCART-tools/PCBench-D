    def _can_hold_element(self, element):
        tipo = maybe_infer_dtype_type(element)
        if tipo is not None:
            return (issubclass(tipo.type, np.integer) and
                    not issubclass(tipo.type, (np.datetime64,
                                               np.timedelta64)) and
                    self.dtype.itemsize >= tipo.itemsize)
        return is_integer(element)
