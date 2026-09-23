    def set_table_styles(
        self,
        table_styles: dict[Any, CSSStyles] | CSSStyles,
        axis: int = 0,
        overwrite: bool = True,
    ) -> Styler:
        """
        Set the table styles included within the ``<style>`` HTML element.

        This function can be used to style the entire table, columns, rows or
        specific HTML selectors.

        Parameters
        ----------
        table_styles : list or dict
            If supplying a list, each individual table_style should be a
            dictionary with ``selector`` and ``props`` keys. ``selector``
            should be a CSS selector that the style will be applied to
            (automatically prefixed by the table's UUID) and ``props``
            should be a list of tuples with ``(attribute, value)``.
            If supplying a dict, the dict keys should correspond to
            column names or index values, depending upon the specified
            `axis` argument. These will be mapped to row or col CSS
            selectors. MultiIndex values as dict keys should be
            in their respective tuple form. The dict values should be
            a list as specified in the form with CSS selectors and
            props that will be applied to the specified row or column.

            .. versionchanged:: 1.2.0

        axis : {0 or 'index', 1 or 'columns', None}, default 0
            Apply to each column (``axis=0`` or ``'index'``), to each row
            (``axis=1`` or ``'columns'``). Only used if `table_styles` is
            dict.

            .. versionadded:: 1.2.0

        overwrite : bool, default True
            Styles are replaced if `True`, or extended if `False`. CSS
            rules are preserved so most recent styles set will dominate
            if selectors intersect.

            .. versionadded:: 1.2.0

        Returns
        -------
        self : Styler

        See Also
        --------
        Styler.set_td_classes: Set the DataFrame of strings added to the ``class``
            attribute of ``<td>`` HTML elements.
        Styler.set_table_attributes: Set the table attributes added to the ``<table>``
            HTML element.

        Examples
        --------
        >>> df = pd.DataFrame(np.random.randn(10, 4),
        ...                   columns=['A', 'B', 'C', 'D'])
        >>> df.style.set_table_styles(
        ...     [{'selector': 'tr:hover',
        ...       'props': [('background-color', 'yellow')]}]
        ... )

        Or with CSS strings

        >>> df.style.set_table_styles(
        ...     [{'selector': 'tr:hover',
        ...       'props': 'background-color: yellow; font-size: 1em;']}]
        ... )

        Adding column styling by name

        >>> df.style.set_table_styles({
        ...     'A': [{'selector': '',
        ...            'props': [('color', 'red')]}],
        ...     'B': [{'selector': 'td',
        ...            'props': 'color: blue;']}]
        ... }, overwrite=False)

        Adding row styling

        >>> df.style.set_table_styles({
        ...     0: [{'selector': 'td:hover',
        ...          'props': [('font-size', '25px')]}]
        ... }, axis=1, overwrite=False)
        """
        if isinstance(table_styles, dict):
            if axis in [0, "index"]:
                obj, idf = self.data.columns, ".col"
            else:
                obj, idf = self.data.index, ".row"

            table_styles = [
                {
                    "selector": str(s["selector"]) + idf + str(idx),
                    "props": maybe_convert_css_to_tuples(s["props"]),
                }
                for key, styles in table_styles.items()
                for idx in obj.get_indexer_for([key])
                for s in styles
            ]
        else:
            table_styles = [
                {
                    "selector": s["selector"],
                    "props": maybe_convert_css_to_tuples(s["props"]),
                }
                for s in table_styles
            ]

        if not overwrite and self.table_styles is not None:
            self.table_styles.extend(table_styles)
        else:
            self.table_styles = table_styles
        return self
