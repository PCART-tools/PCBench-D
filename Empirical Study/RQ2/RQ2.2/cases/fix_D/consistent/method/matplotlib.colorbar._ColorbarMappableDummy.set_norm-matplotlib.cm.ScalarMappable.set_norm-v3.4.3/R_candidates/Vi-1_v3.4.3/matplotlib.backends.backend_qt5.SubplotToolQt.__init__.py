    def __init__(self, targetfig, parent):
        super().__init__(None)

        self._figure = targetfig

        for lower, higher in [("bottom", "top"), ("left", "right")]:
            self._widgets[lower].valueChanged.connect(
                lambda val: self._widgets[higher].setMinimum(val + .001))
            self._widgets[higher].valueChanged.connect(
                lambda val: self._widgets[lower].setMaximum(val - .001))

        self._attrs = ["top", "bottom", "left", "right", "hspace", "wspace"]
        self._defaults = {attr: vars(self._figure.subplotpars)[attr]
                          for attr in self._attrs}

        # Set values after setting the range callbacks, but before setting up
        # the redraw callbacks.
        self._reset()

        for attr in self._attrs:
            self._widgets[attr].valueChanged.connect(self._on_value_changed)
        for action, method in [("Export values", self._export_values),
                               ("Tight layout", self._tight_layout),
                               ("Reset", self._reset),
                               ("Close", self.close)]:
            self._widgets[action].clicked.connect(method)
