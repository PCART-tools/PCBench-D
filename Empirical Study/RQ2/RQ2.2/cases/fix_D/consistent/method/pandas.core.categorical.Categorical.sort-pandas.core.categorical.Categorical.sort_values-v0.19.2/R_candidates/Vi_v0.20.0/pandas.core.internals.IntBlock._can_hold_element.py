    def _can_hold_element(self, element):
        if is_list_like(element):
            element = np.array(element)
            tipo = element.dtype.type
            return (issubclass(tipo, np.integer) and
                    not issubclass(tipo, (np.datetime64, np.timedelta64)))
        return is_integer(element)
