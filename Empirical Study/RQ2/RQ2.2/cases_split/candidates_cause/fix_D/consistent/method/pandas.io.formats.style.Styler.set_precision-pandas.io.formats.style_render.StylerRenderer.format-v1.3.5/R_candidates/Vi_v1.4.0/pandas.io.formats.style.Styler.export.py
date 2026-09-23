    def export(self) -> dict[str, Any]:
        """
        Export the styles applied to the current Styler.

        Can be applied to a second Styler with ``Styler.use``.

        Returns
        -------
        styles : dict

        See Also
        --------
        Styler.use: Set the styles on the current Styler.
        Styler.copy: Create a copy of the current Styler.

        Notes
        -----
        This method is designed to copy non-data dependent attributes of
        one Styler to another. It differs from ``Styler.copy`` where data and
        data dependent attributes are also copied.

        The following items are exported since they are not generally data dependent:

          - Styling functions added by the ``apply`` and ``applymap``
          - Whether axes and names are hidden from the display, if unambiguous.
          - Table attributes
          - Table styles

        The following attributes are considered data dependent and therefore not
        exported:

          - Caption
          - UUID
          - Tooltips
          - Any hidden rows or columns identified by Index labels
          - Any formatting applied using ``Styler.format``
          - Any CSS classes added using ``Styler.set_td_classes``

        Examples
        --------

        >>> styler = DataFrame([[1, 2], [3, 4]]).style
        >>> styler2 = DataFrame([[9, 9, 9]]).style
        >>> styler.hide(axis=0).highlight_max(axis=1)  # doctest: +SKIP
        >>> export = styler.export()
        >>> styler2.use(export)  # doctest: +SKIP
        """
        return {
            "apply": copy.copy(self._todo),
            "table_attributes": self.table_attributes,
            "table_styles": copy.copy(self.table_styles),
            "hide_index": all(self.hide_index_),
            "hide_columns": all(self.hide_columns_),
            "hide_index_names": self.hide_index_names,
            "hide_column_names": self.hide_column_names,
            "css": copy.copy(self.css),
        }
