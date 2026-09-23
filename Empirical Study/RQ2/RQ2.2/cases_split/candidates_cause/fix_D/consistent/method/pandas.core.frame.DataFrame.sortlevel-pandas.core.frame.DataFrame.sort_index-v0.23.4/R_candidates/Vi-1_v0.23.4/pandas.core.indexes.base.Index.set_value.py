    def set_value(self, arr, key, value):
        """
        Fast lookup of value from 1-dimensional ndarray. Only use this if you
        know what you're doing
        """
        self._engine.set_value(com._values_from_object(arr),
                               com._values_from_object(key), value)
