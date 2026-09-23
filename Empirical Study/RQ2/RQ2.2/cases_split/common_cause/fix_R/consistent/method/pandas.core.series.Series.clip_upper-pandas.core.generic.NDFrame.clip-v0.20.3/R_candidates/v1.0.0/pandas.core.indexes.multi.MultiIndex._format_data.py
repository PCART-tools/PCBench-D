    def _format_data(self, name=None):
        """
        Return the formatted data as a unicode string
        """
        return format_object_summary(
            self, self._formatter_func, name=name, line_break_each_value=True
        )
