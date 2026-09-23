    def __init__(self, xy, width, height,
                 edgecolor='k', facecolor='w',
                 fill=True,
                 text='',
                 loc=None,
                 fontproperties=None
                 ):

        # Call base
        Rectangle.__init__(self, xy, width=width, height=height,
                           edgecolor=edgecolor, facecolor=facecolor)
        self.set_clip_on(False)

        # Create text object
        if loc is None:
            loc = 'right'
        self._loc = loc
        self._text = Text(x=xy[0], y=xy[1], text=text,
                          fontproperties=fontproperties)
        self._text.set_clip_on(False)
