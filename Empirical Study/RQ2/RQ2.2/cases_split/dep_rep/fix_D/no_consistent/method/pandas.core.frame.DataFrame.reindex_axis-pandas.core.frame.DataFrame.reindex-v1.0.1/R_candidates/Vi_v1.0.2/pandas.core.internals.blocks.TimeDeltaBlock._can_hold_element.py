    def _can_hold_element(self, element: Any) -> bool:
        tipo = maybe_infer_dtype_type(element)
        if tipo is not None:
            return issubclass(tipo.type, np.timedelta64)
        elif element is NaT:
            return True
        elif isinstance(element, (timedelta, np.timedelta64)):
            return True
        return is_valid_nat_for_dtype(element, self.dtype)
