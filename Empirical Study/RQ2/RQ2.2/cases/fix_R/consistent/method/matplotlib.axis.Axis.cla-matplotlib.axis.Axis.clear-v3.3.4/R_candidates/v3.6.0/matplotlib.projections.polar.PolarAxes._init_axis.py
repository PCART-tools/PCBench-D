    def _init_axis(self):
        # This is moved out of __init__ because non-separable axes don't use it
        self.xaxis = ThetaAxis(self)
        self.yaxis = RadialAxis(self)
        # Calling polar_axes.xaxis.clear() or polar_axes.xaxis.clear()
        # results in weird artifacts. Therefore we disable this for
        # now.
        # self.spines['polar'].register_axis(self.yaxis)
        self._update_transScale()
