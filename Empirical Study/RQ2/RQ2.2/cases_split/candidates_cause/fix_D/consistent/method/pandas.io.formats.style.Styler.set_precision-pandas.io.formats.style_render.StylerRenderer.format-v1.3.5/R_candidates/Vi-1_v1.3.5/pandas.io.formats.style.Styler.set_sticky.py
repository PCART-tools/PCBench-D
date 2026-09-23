    def set_sticky(
        self,
        axis: Axis = 0,
        pixel_size: int | None = None,
        levels: list[int] | None = None,
    ) -> Styler:
        """
        Add CSS to permanently display the index or column headers in a scrolling frame.

        Parameters
        ----------
        axis : {0 or 'index', 1 or 'columns'}, default 0
            Whether to make the index or column headers sticky.
        pixel_size : int, optional
            Required to configure the width of index cells or the height of column
            header cells when sticking a MultiIndex (or with a named Index).
            Defaults to 75 and 25 respectively.
        levels : list of int
            If ``axis`` is a MultiIndex the specific levels to stick. If ``None`` will
            stick all levels.

        Returns
        -------
        self : Styler

        Notes
        -----
        This method uses the CSS 'position: sticky;' property to display. It is
        designed to work with visible axes, therefore both:

          - `styler.set_sticky(axis="index").hide_index()`
          - `styler.set_sticky(axis="columns").hide_columns()`

        may produce strange behaviour due to CSS controls with missing elements.
        """
        if axis in [0, "index"]:
            axis, obj = 0, self.data.index
            pixel_size = 75 if not pixel_size else pixel_size
        elif axis in [1, "columns"]:
            axis, obj = 1, self.data.columns
            pixel_size = 25 if not pixel_size else pixel_size
        else:
            raise ValueError("`axis` must be one of {0, 1, 'index', 'columns'}")

        props = "position:sticky; background-color:white;"
        if not isinstance(obj, pd.MultiIndex):
            # handling MultiIndexes requires different CSS

            if axis == 1:
                # stick the first <tr> of <head> and, if index names, the second <tr>
                # if self._hide_columns then no <thead><tr> here will exist: no conflict
                styles: CSSStyles = [
                    {
                        "selector": "thead tr:nth-child(1) th",
                        "props": props + "top:0px; z-index:2;",
                    }
                ]
                if not self.index.names[0] is None:
                    styles[0]["props"] = (
                        props + f"top:0px; z-index:2; height:{pixel_size}px;"
                    )
                    styles.append(
                        {
                            "selector": "thead tr:nth-child(2) th",
                            "props": props
                            + f"top:{pixel_size}px; z-index:2; height:{pixel_size}px; ",
                        }
                    )
            else:
                # stick the first <th> of each <tr> in both <thead> and <tbody>
                # if self._hide_index then no <th> will exist in <tbody>: no conflict
                # but <th> will exist in <thead>: conflict with initial element
                styles = [
                    {
                        "selector": "thead tr th:nth-child(1)",
                        "props": props + "left:0px; z-index:3 !important;",
                    },
                    {
                        "selector": "tbody tr th:nth-child(1)",
                        "props": props + "left:0px; z-index:1;",
                    },
                ]

        else:
            # handle the MultiIndex case
            range_idx = list(range(obj.nlevels))
            levels = sorted(levels) if levels else range_idx

            if axis == 1:
                styles = []
                for i, level in enumerate(levels):
                    styles.append(
                        {
                            "selector": f"thead tr:nth-child({level+1}) th",
                            "props": props
                            + (
                                f"top:{i * pixel_size}px; height:{pixel_size}px; "
                                "z-index:2;"
                            ),
                        }
                    )
                if not all(name is None for name in self.index.names):
                    styles.append(
                        {
                            "selector": f"thead tr:nth-child({obj.nlevels+1}) th",
                            "props": props
                            + (
                                f"top:{(i+1) * pixel_size}px; height:{pixel_size}px; "
                                "z-index:2;"
                            ),
                        }
                    )

            else:
                styles = []
                for i, level in enumerate(levels):
                    props_ = props + (
                        f"left:{i * pixel_size}px; "
                        f"min-width:{pixel_size}px; "
                        f"max-width:{pixel_size}px; "
                    )
                    styles.extend(
                        [
                            {
                                "selector": f"thead tr th:nth-child({level+1})",
                                "props": props_ + "z-index:3 !important;",
                            },
                            {
                                "selector": f"tbody tr th.level{level}",
                                "props": props_ + "z-index:1;",
                            },
                        ]
                    )

        return self.set_table_styles(styles, overwrite=False)
