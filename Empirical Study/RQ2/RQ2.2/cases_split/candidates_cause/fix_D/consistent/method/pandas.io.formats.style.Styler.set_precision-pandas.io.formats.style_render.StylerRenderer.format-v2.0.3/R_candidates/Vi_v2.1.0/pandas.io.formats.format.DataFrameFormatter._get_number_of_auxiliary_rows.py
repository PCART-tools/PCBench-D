    def _get_number_of_auxiliary_rows(self) -> int:
        """Get number of rows occupied by prompt, dots and dimension info."""
        dot_row = 1
        prompt_row = 1
        num_rows = dot_row + prompt_row

        if self.show_dimensions:
            num_rows += len(self.dimensions_info.splitlines())

        if self.header:
            num_rows += 1

        return num_rows
