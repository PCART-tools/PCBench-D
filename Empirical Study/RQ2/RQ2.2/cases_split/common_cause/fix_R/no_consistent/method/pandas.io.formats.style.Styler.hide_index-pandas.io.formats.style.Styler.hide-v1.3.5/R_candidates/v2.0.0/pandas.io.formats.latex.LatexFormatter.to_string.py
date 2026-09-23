    def to_string(self) -> str:
        """
        Render a DataFrame to a LaTeX tabular, longtable, or table/tabular
        environment output.
        """
        return self.builder.get_result()
