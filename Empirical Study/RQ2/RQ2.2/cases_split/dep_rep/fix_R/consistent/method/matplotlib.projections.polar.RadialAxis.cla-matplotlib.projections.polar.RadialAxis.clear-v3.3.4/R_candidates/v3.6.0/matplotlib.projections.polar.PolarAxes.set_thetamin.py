    def set_thetamin(self, thetamin):
        """Set the minimum theta limit in degrees."""
        self.viewLim.x0 = np.deg2rad(thetamin)
