    def __init__(self, line):
        """
        Initialize the class with a `.Line2D` instance.  The line should
        already be added to some :class:`matplotlib.axes.Axes` instance and
        should have the picker property set.
        """
        if line.axes is None:
            raise RuntimeError('You must first add the line to the Axes')

        if line.get_picker() is None:
            raise RuntimeError('You must first set the picker property '
                               'of the line')

        self.axes = line.axes
        self.line = line
        self.canvas = self.axes.figure.canvas
        self.cid = self.canvas.mpl_connect('pick_event', self.onpick)

        self.ind = set()
