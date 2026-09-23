    def __repr__(self) -> str:
        # the short repr has no trailing newline, while the truncated
        # repr does. So we include a newline in our template, and strip
        # any trailing newlines from format_object_summary
        data = self._format_data()
        class_name = f"<{type(self).__name__}>\n"

        template = (
            f"{class_name}"
            f"{data}\n"
            f"Length: {len(self)}, closed: {self.closed}, dtype: {self.dtype}"
        )
        return template
