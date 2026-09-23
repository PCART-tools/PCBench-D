    @staticmethod
    def _parse_subtype(dtype: str) -> Tuple[str, bool]:
        """
        Parse a string to get the subtype

        Parameters
        ----------
        dtype : str
            A string like

            * Sparse[subtype]
            * Sparse[subtype, fill_value]

        Returns
        -------
        subtype : str

        Raises
        ------
        ValueError
            When the subtype cannot be extracted.
        """
        xpr = re.compile(r"Sparse\[(?P<subtype>[^,]*)(, )?(?P<fill_value>.*?)?\]$")
        m = xpr.match(dtype)
        has_fill_value = False
        if m:
            subtype = m.groupdict()["subtype"]
            has_fill_value = bool(m.groupdict()["fill_value"])
        elif dtype == "Sparse":
            subtype = "float64"
        else:
            raise ValueError(f"Cannot parse {dtype}")
        return subtype, has_fill_value
