    def to_string(self) -> str:
        text = self._get_string_representation()
        if self.fmt.should_show_dimensions:
            text = "".join([text, self.fmt.dimensions_info])
        return text
