    def bar(
        self,
        subset: Subset | None = None,
        axis: Axis | None = 0,
        color="#d65f5f",
        width: float = 100,
        align: str = "left",
        vmin: float | None = None,
        vmax: float | None = None,
    ) -> Styler:
        """
        Draw bar chart in the cell backgrounds.

        Parameters
        ----------
        subset : label, array-like, IndexSlice, optional
            A valid 2d input to `DataFrame.loc[<subset>]`, or, in the case of a 1d input
            or single key, to `DataFrame.loc[:, <subset>]` where the columns are
            prioritised, to limit ``data`` to *before* applying the function.
        axis : {0 or 'index', 1 or 'columns', None}, default 0
            Apply to each column (``axis=0`` or ``'index'``), to each row
            (``axis=1`` or ``'columns'``), or to the entire DataFrame at once
            with ``axis=None``.
        color : str or 2-tuple/list
            If a str is passed, the color is the same for both
            negative and positive numbers. If 2-tuple/list is used, the
            first element is the color_negative and the second is the
            color_positive (eg: ['#d65f5f', '#5fba7d']).
        width : float, default 100
            A number between 0 or 100. The largest value will cover `width`
            percent of the cell's width.
        align : {'left', 'zero',' mid'}, default 'left'
            How to align the bars with the cells.

            - 'left' : the min value starts at the left of the cell.
            - 'zero' : a value of zero is located at the center of the cell.
            - 'mid' : the center of the cell is at (max-min)/2, or
              if values are all negative (positive) the zero is aligned
              at the right (left) of the cell.
        vmin : float, optional
            Minimum bar value, defining the left hand limit
            of the bar drawing range, lower values are clipped to `vmin`.
            When None (default): the minimum value of the data will be used.
        vmax : float, optional
            Maximum bar value, defining the right hand limit
            of the bar drawing range, higher values are clipped to `vmax`.
            When None (default): the maximum value of the data will be used.

        Returns
        -------
        self : Styler
        """
        if align not in ("left", "zero", "mid"):
            raise ValueError("`align` must be one of {'left', 'zero',' mid'}")

        if not (is_list_like(color)):
            color = [color, color]
        elif len(color) == 1:
            color = [color[0], color[0]]
        elif len(color) > 2:
            raise ValueError(
                "`color` must be string or a list-like "
                "of length 2: [`color_neg`, `color_pos`] "
                "(eg: color=['#d65f5f', '#5fba7d'])"
            )

        if subset is None:
            subset = self.data.select_dtypes(include=np.number).columns

        self.apply(
            self._bar,
            subset=subset,
            axis=axis,
            align=align,
            colors=color,
            width=width,
            vmin=vmin,
            vmax=vmax,
        )

        return self
