    def __repr__(self):
        from pandas.io.formats.printing import format_object_summary

        template = "{class_name}" "{data}\n" "Length: {length}, dtype: {dtype}"
        # the short repr has no trailing newline, while the truncated
        # repr does. So we include a newline in our template, and strip
        # any trailing newlines from format_object_summary
        data = format_object_summary(
            self, self._formatter(), indent_for_name=False
        ).rstrip(", \n")
        class_name = "<{}>\n".format(self.__class__.__name__)
        return template.format(
            class_name=class_name, data=data, length=len(self), dtype=self.dtype
        )
