    @Artist.axes.setter
    def axes(self, ax):
        # call the set method from the base-class property
        Artist.axes.fset(self, ax)
        if ax is not None:
            # connect unit-related callbacks
            if ax.xaxis is not None:
                self._xcid = ax.xaxis.callbacks.connect('units',
                                                        self.recache_always)
            if ax.yaxis is not None:
                self._ycid = ax.yaxis.callbacks.connect('units',
                                                        self.recache_always)
