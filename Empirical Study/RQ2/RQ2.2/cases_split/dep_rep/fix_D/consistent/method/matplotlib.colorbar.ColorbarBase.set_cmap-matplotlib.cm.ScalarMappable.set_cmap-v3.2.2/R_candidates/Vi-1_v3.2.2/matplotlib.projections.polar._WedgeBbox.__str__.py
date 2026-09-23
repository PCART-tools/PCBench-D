    def __str__(self):
        return ("{}(\n"
                    "{},\n"
                    "{},\n"
                    "{})"
                .format(type(self).__name__,
                        mtransforms._indent_str(self._center),
                        mtransforms._indent_str(self._viewLim),
                        mtransforms._indent_str(self._originLim)))
