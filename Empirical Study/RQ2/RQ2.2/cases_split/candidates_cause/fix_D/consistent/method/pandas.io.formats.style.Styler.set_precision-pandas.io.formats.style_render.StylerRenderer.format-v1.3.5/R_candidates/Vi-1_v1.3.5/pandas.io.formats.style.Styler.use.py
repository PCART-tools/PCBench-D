    def use(self, styles: list[tuple[Callable, tuple, dict]]) -> Styler:
        """
        Set the styles on the current ``Styler``.

        Possibly uses styles from ``Styler.export``.

        Parameters
        ----------
        styles : list
            List of style functions.

        Returns
        -------
        self : Styler

        See Also
        --------
        Styler.export : Export the styles to applied to the current ``Styler``.
        """
        self._todo.extend(styles)
        return self
