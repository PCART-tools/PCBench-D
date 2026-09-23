    def _can_hold_element(self, element):
        if is_list_like(element):
            element = np.array(element)
            return issubclass(element.dtype.type, np.integer)
        return com.is_integer(element)
