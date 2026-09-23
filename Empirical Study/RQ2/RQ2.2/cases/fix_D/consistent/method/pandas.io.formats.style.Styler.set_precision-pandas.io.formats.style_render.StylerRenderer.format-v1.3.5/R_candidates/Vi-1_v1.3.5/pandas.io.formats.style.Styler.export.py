    def export(self) -> list[tuple[Callable, tuple, dict]]:
        """
        Export the styles applied to the current ``Styler``.

        Can be applied to a second Styler with ``Styler.use``.

        Returns
        -------
        styles : list

        See Also
        --------
        Styler.use: Set the styles on the current ``Styler``.
        """
        return self._todo
