    def _can_hold_element(self, element):
        if is_list_like(element):
            element = np.array(element)
            tipo = element.dtype.type
            return (issubclass(tipo, (np.floating, np.integer)) and
                    not issubclass(tipo, (np.datetime64, np.timedelta64)))
        return (isinstance(element, (float, int, np.float_, np.int_)) and
                not isinstance(element, (bool, np.bool_, datetime, timedelta,
                                         np.datetime64, np.timedelta64)))
