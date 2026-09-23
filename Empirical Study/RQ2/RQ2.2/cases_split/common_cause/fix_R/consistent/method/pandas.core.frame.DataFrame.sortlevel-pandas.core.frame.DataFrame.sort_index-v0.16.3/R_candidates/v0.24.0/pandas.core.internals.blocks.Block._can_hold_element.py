    def _can_hold_element(self, element):
        """ require the same dtype as ourselves """
        dtype = self.values.dtype.type
        tipo = maybe_infer_dtype_type(element)
        if tipo is not None:
            return issubclass(tipo.type, dtype)
        return isinstance(element, dtype)
