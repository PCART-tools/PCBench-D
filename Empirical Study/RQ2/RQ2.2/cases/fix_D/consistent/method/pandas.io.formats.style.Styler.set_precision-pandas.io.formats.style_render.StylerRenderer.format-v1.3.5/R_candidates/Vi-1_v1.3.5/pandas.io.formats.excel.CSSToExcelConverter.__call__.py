    def __call__(self, declarations_str: str) -> dict[str, dict[str, str]]:
        """
        Convert CSS declarations to ExcelWriter style.

        Parameters
        ----------
        declarations_str : str
            List of CSS declarations.
            e.g. "font-weight: bold; background: blue"

        Returns
        -------
        xlstyle : dict
            A style as interpreted by ExcelWriter when found in
            ExcelCell.style.
        """
        # TODO: memoize?
        properties = self.compute_css(declarations_str, self.inherited)
        return self.build_xlstyle(properties)
