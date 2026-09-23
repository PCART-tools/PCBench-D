    def _can_hold_element(self, element):
        tipo = maybe_infer_dtype_type(element)
        if tipo is not None:
            return tipo == _NS_DTYPE or tipo == np.int64
        return (is_integer(element) or isinstance(element, datetime) or
                isna(element))
