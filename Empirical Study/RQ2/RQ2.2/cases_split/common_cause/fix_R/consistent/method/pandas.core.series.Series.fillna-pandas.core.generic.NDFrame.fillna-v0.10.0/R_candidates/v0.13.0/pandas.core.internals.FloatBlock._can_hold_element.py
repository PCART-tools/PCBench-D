    def _can_hold_element(self, element):
        if is_list_like(element):
            element = np.array(element)
            return issubclass(element.dtype.type, (np.floating, np.integer))
        return (isinstance(element, (float, int, np.float_, np.int_)) and
                not isinstance(bool, np.bool_))
