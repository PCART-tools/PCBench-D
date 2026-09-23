    def __init__(self):
        self._stale = True
        self.stale_callback = None
        self._axes = None
        self.figure = None

        self._transform = None
        self._transformSet = False
        self._visible = True
        self._animated = False
        self._alpha = None
        self.clipbox = None
        self._clippath = None
        self._clipon = True
        self._label = ''
        self._picker = None
        self._contains = None
        self._rasterized = None
        self._agg_filter = None
        self._mouseover = False
        self.eventson = False  # fire events only if eventson
        self._oid = 0  # an observer id
        self._propobservers = {}  # a dict from oids to funcs
        try:
            self.axes = None
        except AttributeError:
            # Handle self.axes as a read-only property, as in Figure.
            pass
        self._remove_method = None
        self._url = None
        self._gid = None
        self._snap = None
        self._sketch = rcParams['path.sketch']
        self._path_effects = rcParams['path.effects']
        self._sticky_edges = _XYPair([], [])
