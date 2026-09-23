    def set_thetamax(self, thetamax):
        """Set the maximum theta limit in degrees."""
        self.viewLim.x1 = np.deg2rad(thetamax)
