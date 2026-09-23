    def add_object_type_line(self) -> None:
        """Add line with string representation of dataframe to the table."""
        self._lines.append(str(type(self.data)))
