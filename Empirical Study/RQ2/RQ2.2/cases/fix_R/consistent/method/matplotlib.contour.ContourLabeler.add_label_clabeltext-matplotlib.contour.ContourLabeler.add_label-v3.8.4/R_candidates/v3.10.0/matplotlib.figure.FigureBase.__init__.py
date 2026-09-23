    def __init__(self, **kwargs):
        super().__init__()
        # remove the non-figure artist _axes property
        # as it makes no sense for a figure to be _in_ an Axes
        # this is used by the property methods in the artist base class
        # which are over-ridden in this class
        del self._axes

        self._suptitle = None
        self._supxlabel = None
        self._supylabel = None

        # groupers to keep track of x, y labels and title we want to align.
        # see self.align_xlabels, self.align_ylabels,
        # self.align_titles, and axis._get_tick_boxes_siblings
        self._align_label_groups = {
            "x": cbook.Grouper(),
            "y": cbook.Grouper(),
            "title": cbook.Grouper()
        }

        self._localaxes = []  # track all Axes
        self.artists = []
        self.lines = []
        self.patches = []
        self.texts = []
        self.images = []
        self.legends = []
        self.subfigs = []
        self.stale = True
        self.suppressComposite = None
        self.set(**kwargs)
