    def other_namespaces(self) -> dict:
        """
        Define other namespaces.

        This method will build dictionary of namespaces attributes
        for root element, conditionally with optional namespaces and
        prefix.
        """

        nmsp_dict: dict[str, str] = {}
        if self.namespaces and self.prefix is None:
            nmsp_dict = {"xmlns": n for p, n in self.namespaces.items() if p != ""}

        if self.namespaces and self.prefix:
            nmsp_dict = {"xmlns": n for p, n in self.namespaces.items() if p == ""}

        return nmsp_dict
