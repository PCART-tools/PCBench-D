    def __init__(self,
                 x=0, y=0, text='',
                 color=None,           # defaults to rc params
                 verticalalignment='baseline',
                 horizontalalignment='left',
                 multialignment=None,
                 fontproperties=None,  # defaults to FontProperties()
                 rotation=None,
                 linespacing=None,
                 rotation_mode=None,
                 usetex=None,          # defaults to rcParams['text.usetex']
                 wrap=False,
                 **kwargs
                 ):
        """
        Create a `.Text` instance at *x*, *y* with string *text*.

        Valid keyword arguments are:

        %(Text)s
        """
        Artist.__init__(self)
        self._x, self._y = x, y

        if color is None:
            color = rcParams['text.color']
        if fontproperties is None:
            fontproperties = FontProperties()
        elif isinstance(fontproperties, str):
            fontproperties = FontProperties(fontproperties)

        self._text = ''
        self.set_text(text)
        self.set_color(color)
        self.set_usetex(usetex)
        self.set_wrap(wrap)
        self.set_verticalalignment(verticalalignment)
        self.set_horizontalalignment(horizontalalignment)
        self._multialignment = multialignment
        self._rotation = rotation
        self._fontproperties = fontproperties
        self._bbox_patch = None  # a FancyBboxPatch instance
        self._renderer = None
        if linespacing is None:
            linespacing = 1.2   # Maybe use rcParam later.
        self._linespacing = linespacing
        self.set_rotation_mode(rotation_mode)
        self.update(kwargs)
