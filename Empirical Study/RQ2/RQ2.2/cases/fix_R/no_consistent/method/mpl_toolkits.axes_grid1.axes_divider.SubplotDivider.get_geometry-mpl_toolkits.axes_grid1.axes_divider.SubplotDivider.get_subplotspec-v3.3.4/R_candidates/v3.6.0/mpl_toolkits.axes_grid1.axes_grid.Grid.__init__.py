    def __init__(self, fig,
                 rect,
                 nrows_ncols,
                 ngrids=None,
                 direction="row",
                 axes_pad=0.02,
                 *,
                 share_all=False,
                 share_x=True,
                 share_y=True,
                 label_mode="L",
                 axes_class=None,
                 aspect=False,
                 ):
        """
        Parameters
        ----------
        fig : `.Figure`
            The parent figure.
        rect : (float, float, float, float) or int
            The axes position, as a ``(left, bottom, width, height)`` tuple or
            as a three-digit subplot position code (e.g., "121").
        nrows_ncols : (int, int)
            Number of rows and columns in the grid.
        ngrids : int or None, default: None
            If not None, only the first *ngrids* axes in the grid are created.
        direction : {"row", "column"}, default: "row"
            Whether axes are created in row-major ("row by row") or
            column-major order ("column by column").  This also affects the
            order in which axes are accessed using indexing (``grid[index]``).
        axes_pad : float or (float, float), default: 0.02
            Padding or (horizontal padding, vertical padding) between axes, in
            inches.
        share_all : bool, default: False
            Whether all axes share their x- and y-axis.  Overrides *share_x*
            and *share_y*.
        share_x : bool, default: True
            Whether all axes of a column share their x-axis.
        share_y : bool, default: True
            Whether all axes of a row share their y-axis.
        label_mode : {"L", "1", "all"}, default: "L"
            Determines which axes will get tick labels:

            - "L": All axes on the left column get vertical tick labels;
              all axes on the bottom row get horizontal tick labels.
            - "1": Only the bottom left axes is labelled.
            - "all": all axes are labelled.

        axes_class : subclass of `matplotlib.axes.Axes`, default: None
        aspect : bool, default: False
            Whether the axes aspect ratio follows the aspect ratio of the data
            limits.
        """
        self._nrows, self._ncols = nrows_ncols

        if ngrids is None:
            ngrids = self._nrows * self._ncols
        else:
            if not 0 < ngrids <= self._nrows * self._ncols:
                raise ValueError(
                    "ngrids must be positive and not larger than nrows*ncols")

        self.ngrids = ngrids

        self._horiz_pad_size, self._vert_pad_size = map(
            Size.Fixed, np.broadcast_to(axes_pad, 2))

        _api.check_in_list(["column", "row"], direction=direction)
        self._direction = direction

        if axes_class is None:
            axes_class = self._defaultAxesClass
        elif isinstance(axes_class, (list, tuple)):
            cls, kwargs = axes_class
            axes_class = functools.partial(cls, **kwargs)

        kw = dict(horizontal=[], vertical=[], aspect=aspect)
        if isinstance(rect, (str, Number, SubplotSpec)):
            self._divider = SubplotDivider(fig, rect, **kw)
        elif len(rect) == 3:
            self._divider = SubplotDivider(fig, *rect, **kw)
        elif len(rect) == 4:
            self._divider = Divider(fig, rect, **kw)
        else:
            raise TypeError("Incorrect rect format")

        rect = self._divider.get_position()

        axes_array = np.full((self._nrows, self._ncols), None, dtype=object)
        for i in range(self.ngrids):
            col, row = self._get_col_row(i)
            if share_all:
                sharex = sharey = axes_array[0, 0]
            else:
                sharex = axes_array[0, col] if share_x else None
                sharey = axes_array[row, 0] if share_y else None
            axes_array[row, col] = axes_class(
                fig, rect, sharex=sharex, sharey=sharey)
        self.axes_all = axes_array.ravel(
            order="C" if self._direction == "row" else "F").tolist()
        self.axes_column = axes_array.T.tolist()
        self.axes_row = axes_array.tolist()
        self.axes_llc = self.axes_column[0][-1]

        self._init_locators()

        for ax in self.axes_all:
            fig.add_axes(ax)

        self.set_label_mode(label_mode)
