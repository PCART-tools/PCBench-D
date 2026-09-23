    def _pseudo_css(self, uuid: str, name: str, row: int, col: int, text: str):
        """
        For every table data-cell that has a valid tooltip (not None, NaN or
        empty string) must create two pseudo CSS entries for the specific
        <td> element id which are added to overall table styles:
        an on hover visibility change and a content change
        dependent upon the user's chosen display string.

        For example:
            [{"selector": "T__row1_col1:hover .pd-t",
             "props": [("visibility", "visible")]},
            {"selector": "T__row1_col1 .pd-t::after",
             "props": [("content", "Some Valid Text String")]}]

        Parameters
        ----------
        uuid: str
            The uuid of the Styler instance
        name: str
            The css-name of the class used for styling tooltips
        row : int
            The row index of the specified tooltip string data
        col : int
            The col index of the specified tooltip string data
        text : str
            The textual content of the tooltip to be displayed in HTML.

        Returns
        -------
        pseudo_css : List
        """
        selector_id = "#T_" + uuid + "row" + str(row) + "_col" + str(col)
        return [
            {
                "selector": selector_id + f":hover .{name}",
                "props": [("visibility", "visible")],
            },
            {
                "selector": selector_id + f" .{name}::after",
                "props": [("content", f'"{text}"')],
            },
        ]
