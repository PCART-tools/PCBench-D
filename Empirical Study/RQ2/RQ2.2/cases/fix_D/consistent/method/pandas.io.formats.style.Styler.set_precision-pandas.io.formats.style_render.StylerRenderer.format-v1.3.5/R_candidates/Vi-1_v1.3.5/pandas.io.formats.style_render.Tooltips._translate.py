    def _translate(self, styler_data: FrameOrSeriesUnion, uuid: str, d: dict):
        """
        Mutate the render dictionary to allow for tooltips:

        - Add ``<span>`` HTML element to each data cells ``display_value``. Ignores
          headers.
        - Add table level CSS styles to control pseudo classes.

        Parameters
        ----------
        styler_data : DataFrame
            Underlying ``Styler`` DataFrame used for reindexing.
        uuid : str
            The underlying ``Styler`` uuid for CSS id.
        d : dict
            The dictionary prior to final render

        Returns
        -------
        render_dict : Dict
        """
        self.tt_data = self.tt_data.reindex_like(styler_data)

        if self.tt_data.empty:
            return d

        name = self.class_name

        mask = (self.tt_data.isna()) | (self.tt_data.eq(""))  # empty string = no ttip
        self.table_styles = [
            style
            for sublist in [
                self._pseudo_css(uuid, name, i, j, str(self.tt_data.iloc[i, j]))
                for i in range(len(self.tt_data.index))
                for j in range(len(self.tt_data.columns))
                if not mask.iloc[i, j]
            ]
            for style in sublist
        ]

        if self.table_styles:
            # add span class to every cell only if at least 1 non-empty tooltip
            for row in d["body"]:
                for item in row:
                    if item["type"] == "td":
                        item["display_value"] = (
                            str(item["display_value"])
                            + f'<span class="{self.class_name}"></span>'
                        )
            d["table_styles"].extend(self._class_styles)
            d["table_styles"].extend(self.table_styles)

        return d
