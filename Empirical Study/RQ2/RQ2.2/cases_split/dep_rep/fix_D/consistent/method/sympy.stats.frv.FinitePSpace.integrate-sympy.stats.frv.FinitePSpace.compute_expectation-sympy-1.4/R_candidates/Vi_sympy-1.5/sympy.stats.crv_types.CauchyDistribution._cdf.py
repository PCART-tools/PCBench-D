    def _cdf(self, x):
        x0, gamma = self.x0, self.gamma
        return (1/pi)*atan((x - x0)/gamma) + S.Half
