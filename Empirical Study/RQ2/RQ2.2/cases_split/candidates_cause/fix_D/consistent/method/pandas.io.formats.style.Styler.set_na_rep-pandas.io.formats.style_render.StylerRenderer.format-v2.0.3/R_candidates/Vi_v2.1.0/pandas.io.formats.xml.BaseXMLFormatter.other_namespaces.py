    def other_namespaces(self) -> dict:
        """
        Define other namespaces.

        This method will build dictionary of namespaces attributes
        for root element, conditionally with optional namespaces and
        prefix.
        """

        nmsp_dict: dict[str, str] = {}
        if self.namespaces:
            nmsp_dict = {
                f"xmlns{p if p=='' else f':{p}'}": n
                for p, n in self.namespaces.items()
                if n != self.prefix_uri[1:-1]
            }

        return nmsp_dict
