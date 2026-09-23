    def _init_axis(self):
        # This is moved out of __init__ because non-separable axes don't use it
        self.xaxis = ThetaAxis(self, clear=False)
        self.yaxis = RadialAxis(self, clear=False)
        self.spines['polar'].register_axis(self.yaxis)
