    @Artist.axes.setter
    def axes(self, ax):
        # call the set method from the base-class property
        Artist.axes.fset(self, ax)
        if ax is not None:
            for axis in ax._get_axis_map().values():
                axis.callbacks._pickled_cids.add(
                    axis.callbacks.connect('units', self.recache_always))
