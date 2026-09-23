    def __init__(self, ax, onselect, direction, minspan=None, useblit=False,
                 rectprops=None, onmove_callback=None, span_stays=False,
                 button=None):

        _SelectorWidget.__init__(self, ax, onselect, useblit=useblit,
                                 button=button)

        if rectprops is None:
            rectprops = dict(facecolor='red', alpha=0.5)

        rectprops['animated'] = self.useblit

        if direction not in ['horizontal', 'vertical']:
            raise ValueError("direction must be 'horizontal' or 'vertical'")
        self.direction = direction

        self.rect = None
        self.pressv = None

        self.rectprops = rectprops
        self.onmove_callback = onmove_callback
        self.minspan = minspan
        self.span_stays = span_stays

        # Needed when dragging out of axes
        self.prev = (0, 0)

        # Reset canvas so that `new_axes` connects events.
        self.canvas = None
        self.new_axes(ax)
