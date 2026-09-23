    def _can_hold_element(self, element: Any) -> bool:
        tipo = maybe_infer_dtype_type(element)
        if tipo is not None:
            return issubclass(tipo.type, (np.floating, np.integer)) and not issubclass(
                tipo.type, (np.datetime64, np.timedelta64)
            )
        return isinstance(
            element, (float, int, np.floating, np.int_)
        ) and not isinstance(
            element,
            (bool, np.bool_, datetime, timedelta, np.datetime64, np.timedelta64),
        )
