    def _can_hold_element(self, element):
        if is_list_like(element):
            element = np.array(element)
            return element.dtype == _NS_DTYPE or element.dtype == np.int64
        return (is_integer(element) or isinstance(element, datetime) or
                isnull(element))
