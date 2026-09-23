    def format(
        self,
        name: bool = False,
        formatter: Optional[Callable] = None,
        na_rep: str = "NaT",
        date_format: Optional[str] = None,
    ) -> List[str]:
        """
        Render a string representation of the Index.
        """
        header = []
        if name:
            header.append(
                ibase.pprint_thing(self.name, escape_chars=("\t", "\r", "\n"))
                if self.name is not None
                else ""
            )

        if formatter is not None:
            return header + list(self.map(formatter))

        return self._format_with_header(header, na_rep=na_rep, date_format=date_format)
