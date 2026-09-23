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
