class Cell(Rectangle):
    """
    A cell is a `.Rectangle` with some associated `.Text`.

    As a user, you'll most likely not creates cells yourself. Instead, you
    should use either the `~matplotlib.table.table` factory function or
    `.Table.add_cell`.
    """

    PAD = 0.1
    """Padding between text and rectangle."""

    _edges = 'BRTL'
    _edge_aliases = {'open':         '',
                     'closed':       _edges,  # default
                     'horizontal':   'BT',
                     'vertical':     'RL'
                     }

    def __init__(self, xy, width, height,
                 edgecolor='k', facecolor='w',
                 fill=True,
                 text='',
                 loc=None,
                 fontproperties=None,
                 *,
                 visible_edges='closed',
                 ):
        """
        Parameters
        ----------
        xy : 2-tuple
            The position of the bottom left corner of the cell.
        width : float
            The cell width.
        height : float
            The cell height.
        edgecolor : color
            The color of the cell border.
        facecolor : color
            The cell facecolor.
        fill : bool
            Whether the cell background is filled.
        text : str
            The cell text.
        loc : {'left', 'center', 'right'}, default: 'right'
            The alignment of the text within the cell.
        fontproperties : dict
            A dict defining the font properties of the text. Supported keys and
            values are the keyword arguments accepted by `.FontProperties`.
        visible_edges : str, default: 'closed'
            The cell edges to be drawn with a line: a substring of 'BRTL'
            (bottom, right, top, left), or one of 'open' (no edges drawn),
            'closed' (all edges drawn), 'horizontal' (bottom and top),
            'vertical' (right and left).
        """

        # Call base
        super().__init__(xy, width=width, height=height, fill=fill,
                         edgecolor=edgecolor, facecolor=facecolor)
        self.set_clip_on(False)
        self.visible_edges = visible_edges

        # Create text object
        if loc is None:
            loc = 'right'
        self._loc = loc
        self._text = Text(x=xy[0], y=xy[1], clip_on=False,
                          text=text, fontproperties=fontproperties,
                          horizontalalignment=loc, verticalalignment='center')

    def set_transform(self, trans):
        super().set_transform(trans)
        # the text does not get the transform!
        self.stale = True

    def set_figure(self, fig):
        super().set_figure(fig)
        self._text.set_figure(fig)

    def get_text(self):
        """Return the cell `.Text` instance."""
        return self._text

    def set_fontsize(self, size):
        """Set the text fontsize."""
        self._text.set_fontsize(size)
        self.stale = True

    def get_fontsize(self):
        """Return the cell fontsize."""
        return self._text.get_fontsize()

    def auto_set_font_size(self, renderer):
        """Shrink font size until the text fits into the cell width."""
        fontsize = self.get_fontsize()
        required = self.get_required_width(renderer)
        while fontsize > 1 and required > self.get_width():
            fontsize -= 1
            self.set_fontsize(fontsize)
            required = self.get_required_width(renderer)

        return fontsize

    @allow_rasterization
    def draw(self, renderer):
        if not self.get_visible():
            return
        # draw the rectangle
        super().draw(renderer)
        # position the text
        self._set_text_position(renderer)
        self._text.draw(renderer)
        self.stale = False

    def _set_text_position(self, renderer):
        """Set text up so it is drawn in the right place."""
        bbox = self.get_window_extent(renderer)
        # center vertically
        y = bbox.y0 + bbox.height / 2
        # position horizontally
        loc = self._text.get_horizontalalignment()
        if loc == 'center':
            x = bbox.x0 + bbox.width / 2
        elif loc == 'left':
            x = bbox.x0 + bbox.width * self.PAD
        else:  # right.
            x = bbox.x0 + bbox.width * (1 - self.PAD)
        self._text.set_position((x, y))

    def get_text_bounds(self, renderer):
        """
        Return the text bounds as *(x, y, width, height)* in table coordinates.
        """
        return (self._text.get_window_extent(renderer)
                .transformed(self.get_data_transform().inverted())
                .bounds)

    def get_required_width(self, renderer):
        """Return the minimal required width for the cell."""
        l, b, w, h = self.get_text_bounds(renderer)
        return w * (1.0 + (2.0 * self.PAD))

    @docstring.dedent_interpd
    def set_text_props(self, **kwargs):
        """
        Update the text properties.

        Valid keyword arguments are:

        %(Text_kwdoc)s
        """
        self._text.update(kwargs)
        self.stale = True

    @property
    def visible_edges(self):
        """
        The cell edges to be drawn with a line.

        Reading this property returns a substring of 'BRTL' (bottom, right,
        top, left').

        When setting this property, you can use a substring of 'BRTL' or one
        of {'open', 'closed', 'horizontal', 'vertical'}.
        """
        return self._visible_edges

    @visible_edges.setter
    def visible_edges(self, value):
        if value is None:
            self._visible_edges = self._edges
        elif value in self._edge_aliases:
            self._visible_edges = self._edge_aliases[value]
        else:
            if any(edge not in self._edges for edge in value):
                raise ValueError('Invalid edge param {}, must only be one of '
                                 '{} or string of {}'.format(
                                     value,
                                     ", ".join(self._edge_aliases),
                                     ", ".join(self._edges)))
            self._visible_edges = value
        self.stale = True

    def get_path(self):
        """Return a `.Path` for the `.visible_edges`."""
        codes = [Path.MOVETO]
        codes.extend(
            Path.LINETO if edge in self._visible_edges else Path.MOVETO
            for edge in self._edges)
        if Path.MOVETO not in codes[1:]:  # All sides are visible
            codes[-1] = Path.CLOSEPOLY
        return Path(
            [[0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0], [0.0, 0.0]],
            codes,
            readonly=True
            )
