    @property
    def direction(self):
        """ The unit vector direction towards the light source """

        # Azimuth is in degrees clockwise from North. Convert to radians
        # counterclockwise from East (mathematical notation).
        az = np.radians(90 - self.azdeg)
        alt = np.radians(self.altdeg)

        return np.array([
            np.cos(az) * np.cos(alt),
            np.sin(az) * np.cos(alt),
            np.sin(alt)
        ])
