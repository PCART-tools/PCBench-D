    def __str__(self):
        return self.__class__.__name__ \
            + "(%f,%f)" % tuple(self.axes.transAxes.transform_point((0, 0)))
