    def __str__(self):
        return ("{}(\n"
                    "{},\n"
                    "{},\n"
                    "{})"
                .format(type(self).__name__,
                        mtransforms._indent_str(self.axes),
                        mtransforms._indent_str(self.pad),
                        mtransforms._indent_str(repr(self.mode))))
