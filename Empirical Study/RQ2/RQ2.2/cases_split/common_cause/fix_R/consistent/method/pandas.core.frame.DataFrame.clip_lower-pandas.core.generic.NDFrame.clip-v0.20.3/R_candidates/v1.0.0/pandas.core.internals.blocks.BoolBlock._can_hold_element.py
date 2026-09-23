    def _can_hold_element(self, element: Any) -> bool:
        tipo = maybe_infer_dtype_type(element)
        if tipo is not None:
            return issubclass(tipo.type, np.bool_)
        return isinstance(element, (bool, np.bool_))
