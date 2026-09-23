    def __str__(self):
        return ("{}(\n"
                    "{})"
                .format(type(self).__name__,
                        _indent_str(self._child)))
