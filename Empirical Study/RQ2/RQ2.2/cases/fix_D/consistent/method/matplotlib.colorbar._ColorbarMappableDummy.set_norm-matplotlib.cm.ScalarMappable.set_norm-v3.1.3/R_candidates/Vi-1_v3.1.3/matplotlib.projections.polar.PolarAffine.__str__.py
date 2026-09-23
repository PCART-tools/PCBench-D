    def __str__(self):
        return ("{}(\n"
                    "{},\n"
                    "{})"
                .format(type(self).__name__,
                        mtransforms._indent_str(self._scale_transform),
                        mtransforms._indent_str(self._limits)))
