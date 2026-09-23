    def _init_axis(self):
        # This is moved out of __init__ because non-separable axes don't use it
        self.xaxis = ThetaAxis(self)
        self.yaxis = RadialAxis(self)
