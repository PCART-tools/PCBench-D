    def __str__(self):
        return ("{}(\n"
                    "{},\n"
                    "{})"
                .format(type(self).__name__,
                        _indent_str(self._x),
                        _indent_str(self._y)))
