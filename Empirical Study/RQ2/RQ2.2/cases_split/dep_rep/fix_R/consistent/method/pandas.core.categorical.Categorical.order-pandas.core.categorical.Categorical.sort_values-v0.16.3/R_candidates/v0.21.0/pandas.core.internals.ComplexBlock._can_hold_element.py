    def _can_hold_element(self, element):
        tipo = maybe_infer_dtype_type(element)
        if tipo is not None:
            return issubclass(tipo.type,
                              (np.floating, np.integer, np.complexfloating))
        return (isinstance(element,
                           (float, int, complex, np.float_, np.int_)) and
                not isinstance(element, (bool, np.bool_)))
