    def _can_hold_element(self, element):
        tipo = maybe_infer_dtype_type(element)
        if tipo is not None:
            # TODO: remove the np.int64 support once coerce_values and
            #  _try_coerce_args both coerce to m8[ns] and not i8.
            return issubclass(tipo.type, (np.timedelta64, np.int64))
        elif element is NaT:
            return True
        elif isinstance(element, (timedelta, np.timedelta64)):
            return True
        elif is_integer(element):
            return element == tslibs.iNaT
        return is_valid_nat_for_dtype(element, self.dtype)
