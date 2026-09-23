    def format(
        self,
        name: bool = False,
        formatter: Callable | None = None,
        na_rep: str_t = "NaN",
    ) -> list[str_t]:
        """
        Render a string representation of the Index.
        """
        header = []
        if name:
            header.append(
                pprint_thing(self.name, escape_chars=("\t", "\r", "\n"))
                if self.name is not None
                else ""
            )

        if formatter is not None:
            return header + list(self.map(formatter))

        return self._format_with_header(header, na_rep=na_rep)
