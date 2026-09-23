    @is_copy.setter
    def is_copy(self, msg):
        warnings.warn("Attribute 'is_copy' is deprecated and will be removed "
                      "in a future version.", FutureWarning, stacklevel=2)
        self._is_copy = msg
