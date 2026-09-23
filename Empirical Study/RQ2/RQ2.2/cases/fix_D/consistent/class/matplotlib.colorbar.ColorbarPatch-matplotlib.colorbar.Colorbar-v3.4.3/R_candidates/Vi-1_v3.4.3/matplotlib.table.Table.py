class Table(Artist):
    """
    A table of cells.

    The table consists of a grid of cells, which are indexed by (row, column).

    For a simple table, you'll have a full grid of cells with indices from
    (0, 0) to (num_rows-1, num_cols-1), in which the cell (0, 0) is positioned
    at the top left. However, you can also add cells with negative indices.
    You don't have to add a cell to every grid position, so you can create
    tables that have holes.

    *Note*: You'll usually not create an empty table from scratch. Instead use
    `~matplotlib.table.table` to create a table from data.
    """
    codes = {'best': 0,
             'upper right':  1,  # default
             'upper left':   2,
             'lower left':   3,
             'lower right':  4,
             'center left':  5,
             'center right': 6,
             'lower center': 7,
             'upper center': 8,
             'center':       9,
             'top right':    10,
             'top left':     11,
             'bottom left':  12,
             'bottom right': 13,
             'right':        14,
             'left':         15,
             'top':          16,
             'bottom':       17,
             }
    """Possible values where to place the table relative to the Axes."""

    FONTSIZE = 10

    AXESPAD = 0.02
    """The border between the Axes and the table edge in Axes units."""

    def __init__(self, ax, loc=None, bbox=None, **kwargs):
        """
        Parameters
        ----------
        ax : `matplotlib.axes.Axes`
            The `~.axes.Axes` to plot the table into.
        loc : str
            The position of the cell with respect to *ax*. This must be one of
            the `~.Table.codes`.
        bbox : `.Bbox` or None
            A bounding box to draw the table into. If this is not *None*, this
            overrides *loc*.

        Other Parameters
        ----------------
        **kwargs
            `.Artist` properties.
        """

        super().__init__()

        if isinstance(loc, str):
            if loc not in self.codes:
                raise ValueError(
                    "Unrecognized location {!r}. Valid locations are\n\t{}"
                    .format(loc, '\n\t'.join(self.codes)))
            loc = self.codes[loc]
        self.set_figure(ax.figure)
        self._axes = ax
        self._loc = loc
        self._bbox = bbox

        # use axes coords
        ax._unstale_viewLim()
        self.set_transform(ax.transAxes)

        self._cells = {}
        self._edges = None
        self._autoColumns = []
        self._autoFontsize = True
        self.update(kwargs)

        self.set_clip_on(False)

    def add_cell(self, row, col, *args, **kwargs):
        """
        Create a cell and add it to the table.

        Parameters
        ----------
        row : int
            Row index.
        col : int
            Column index.
        *args, **kwargs
            All other parameters are passed on to `Cell`.

        Returns
        -------
        `.Cell`
            The created cell.

        """
        xy = (0, 0)
        cell = Cell(xy, visible_edges=self.edges, *args, **kwargs)
        self[row, col] = cell
        return cell

    def __setitem__(self, position, cell):
        """
        Set a custom cell in a given position.
        """
        _api.check_isinstance(Cell, cell=cell)
        try:
            row, col = position[0], position[1]
        except Exception as err:
            raise KeyError('Only tuples length 2 are accepted as '
                           'coordinates') from err
        cell.set_figure(self.figure)
        cell.set_transform(self.get_transform())
        cell.set_clip_on(False)
        self._cells[row, col] = cell
        self.stale = True

    def __getitem__(self, position):
        """Retrieve a custom cell from a given position."""
        return self._cells[position]

    @property
    def edges(self):
        """
        The default value of `~.Cell.visible_edges` for newly added
        cells using `.add_cell`.

        Notes
        -----
        This setting does currently only affect newly created cells using
        `.add_cell`.

        To change existing cells, you have to set their edges explicitly::

            for c in tab.get_celld().values():
                c.visible_edges = 'horizontal'

        """
        return self._edges

    @edges.setter
    def edges(self, value):
        self._edges = value
        self.stale = True

    def _approx_text_height(self):
        return (self.FONTSIZE / 72.0 * self.figure.dpi /
                self._axes.bbox.height * 1.2)

    @allow_rasterization
    def draw(self, renderer):
        # docstring inherited

        # Need a renderer to do hit tests on mouseevent; assume the last one
        # will do
        if renderer is None:
            renderer = self.figure._cachedRenderer
        if renderer is None:
            raise RuntimeError('No renderer defined')

        if not self.get_visible():
            return
        renderer.open_group('table', gid=self.get_gid())
        self._update_positions(renderer)

        for key in sorted(self._cells):
            self._cells[key].draw(renderer)

        renderer.close_group('table')
        self.stale = False

    def _get_grid_bbox(self, renderer):
        """
        Get a bbox, in axes coordinates for the cells.

        Only include those in the range (0, 0) to (maxRow, maxCol).
        """
        boxes = [cell.get_window_extent(renderer)
                 for (row, col), cell in self._cells.items()
                 if row >= 0 and col >= 0]
        bbox = Bbox.union(boxes)
        return bbox.transformed(self.get_transform().inverted())

    def contains(self, mouseevent):
        # docstring inherited
        inside, info = self._default_contains(mouseevent)
        if inside is not None:
            return inside, info
        # TODO: Return index of the cell containing the cursor so that the user
        # doesn't have to bind to each one individually.
        renderer = self.figure._cachedRenderer
        if renderer is not None:
            boxes = [cell.get_window_extent(renderer)
                     for (row, col), cell in self._cells.items()
                     if row >= 0 and col >= 0]
            bbox = Bbox.union(boxes)
            return bbox.contains(mouseevent.x, mouseevent.y), {}
        else:
            return False, {}

    def get_children(self):
        """Return the Artists contained by the table."""
        return list(self._cells.values())

    def get_window_extent(self, renderer):
        """Return the bounding box of the table in window coords."""
        self._update_positions(renderer)
        boxes = [cell.get_window_extent(renderer)
                 for cell in self._cells.values()]
        return Bbox.union(boxes)

    def _do_cell_alignment(self):
        """
        Calculate row heights and column widths; position cells accordingly.
        """
        # Calculate row/column widths
        widths = {}
        heights = {}
        for (row, col), cell in self._cells.items():
            height = heights.setdefault(row, 0.0)
            heights[row] = max(height, cell.get_height())
            width = widths.setdefault(col, 0.0)
            widths[col] = max(width, cell.get_width())

        # work out left position for each column
        xpos = 0
        lefts = {}
        for col in sorted(widths):
            lefts[col] = xpos
            xpos += widths[col]

        ypos = 0
        bottoms = {}
        for row in sorted(heights, reverse=True):
            bottoms[row] = ypos
            ypos += heights[row]

        # set cell positions
        for (row, col), cell in self._cells.items():
            cell.set_x(lefts[col])
            cell.set_y(bottoms[row])

    def auto_set_column_width(self, col):
        """
        Automatically set the widths of given columns to optimal sizes.

        Parameters
        ----------
        col : int or sequence of ints
            The indices of the columns to auto-scale.
        """
        # check for col possibility on iteration
        try:
            iter(col)
        except (TypeError, AttributeError):
            self._autoColumns.append(col)
        else:
            for cell in col:
                self._autoColumns.append(cell)

        self.stale = True

    def _auto_set_column_width(self, col, renderer):
        """Automatically set width for column."""
        cells = [cell for key, cell in self._cells.items() if key[1] == col]
        max_width = max((cell.get_required_width(renderer) for cell in cells),
                        default=0)
        for cell in cells:
            cell.set_width(max_width)

    def auto_set_font_size(self, value=True):
        """Automatically set font size."""
        self._autoFontsize = value
        self.stale = True

    def _auto_set_font_size(self, renderer):

        if len(self._cells) == 0:
            return
        fontsize = next(iter(self._cells.values())).get_fontsize()
        cells = []
        for key, cell in self._cells.items():
            # ignore auto-sized columns
            if key[1] in self._autoColumns:
                continue
            size = cell.auto_set_font_size(renderer)
            fontsize = min(fontsize, size)
            cells.append(cell)

        # now set all fontsizes equal
        for cell in self._cells.values():
            cell.set_fontsize(fontsize)

    def scale(self, xscale, yscale):
        """Scale column widths by *xscale* and row heights by *yscale*."""
        for c in self._cells.values():
            c.set_width(c.get_width() * xscale)
            c.set_height(c.get_height() * yscale)

    def set_fontsize(self, size):
        """
        Set the font size, in points, of the cell text.

        Parameters
        ----------
        size : float

        Notes
        -----
        As long as auto font size has not been disabled, the value will be
        clipped such that the text fits horizontally into the cell.

        You can disable this behavior using `.auto_set_font_size`.

        >>> the_table.auto_set_font_size(False)
        >>> the_table.set_fontsize(20)

        However, there is no automatic scaling of the row height so that the
        text may exceed the cell boundary.
        """
        for cell in self._cells.values():
            cell.set_fontsize(size)
        self.stale = True

    def _offset(self, ox, oy):
        """Move all the artists by ox, oy (axes coords)."""
        for c in self._cells.values():
            x, y = c.get_x(), c.get_y()
            c.set_x(x + ox)
            c.set_y(y + oy)

    def _update_positions(self, renderer):
        # called from renderer to allow more precise estimates of
        # widths and heights with get_window_extent

        # Do any auto width setting
        for col in self._autoColumns:
            self._auto_set_column_width(col, renderer)

        if self._autoFontsize:
            self._auto_set_font_size(renderer)

        # Align all the cells
        self._do_cell_alignment()

        bbox = self._get_grid_bbox(renderer)
        l, b, w, h = bbox.bounds

        if self._bbox is not None:
            # Position according to bbox
            rl, rb, rw, rh = self._bbox
            self.scale(rw / w, rh / h)
            ox = rl - l
            oy = rb - b
            self._do_cell_alignment()
        else:
            # Position using loc
            (BEST, UR, UL, LL, LR, CL, CR, LC, UC, C,
             TR, TL, BL, BR, R, L, T, B) = range(len(self.codes))
            # defaults for center
            ox = (0.5 - w / 2) - l
            oy = (0.5 - h / 2) - b
            if self._loc in (UL, LL, CL):   # left
                ox = self.AXESPAD - l
            if self._loc in (BEST, UR, LR, R, CR):  # right
                ox = 1 - (l + w + self.AXESPAD)
            if self._loc in (BEST, UR, UL, UC):     # upper
                oy = 1 - (b + h + self.AXESPAD)
            if self._loc in (LL, LR, LC):           # lower
                oy = self.AXESPAD - b
            if self._loc in (LC, UC, C):            # center x
                ox = (0.5 - w / 2) - l
            if self._loc in (CL, CR, C):            # center y
                oy = (0.5 - h / 2) - b

            if self._loc in (TL, BL, L):            # out left
                ox = - (l + w)
            if self._loc in (TR, BR, R):            # out right
                ox = 1.0 - l
            if self._loc in (TR, TL, T):            # out top
                oy = 1.0 - b
            if self._loc in (BL, BR, B):           # out bottom
                oy = - (b + h)

        self._offset(ox, oy)

    def get_celld(self):
        r"""
        Return a dict of cells in the table mapping *(row, column)* to
        `.Cell`\s.

        Notes
        -----
        You can also directly index into the Table object to access individual
        cells::

            cell = table[row, col]

        """
        return self._cells
