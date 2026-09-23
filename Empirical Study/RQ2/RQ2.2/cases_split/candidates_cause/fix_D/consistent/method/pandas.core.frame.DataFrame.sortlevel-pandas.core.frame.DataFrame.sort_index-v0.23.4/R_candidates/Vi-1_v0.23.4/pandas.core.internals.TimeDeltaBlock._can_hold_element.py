    def _can_hold_element(self, element):
        tipo = maybe_infer_dtype_type(element)
        if tipo is not None:
            return issubclass(tipo.type, np.timedelta64)
        return is_integer(element) or isinstance(
            element, (timedelta, np.timedelta64))
