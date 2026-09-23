    def set_theta_zero_location(self, loc, offset=0.0):
        """
        Sets the location of theta's zero.  (Calls set_theta_offset
        with the correct value in radians under the hood.)

        loc : str
            May be one of "N", "NW", "W", "SW", "S", "SE", "E", or "NE".

        offset : float, optional
            An offset in degrees to apply from the specified `loc`. **Note:**
            this offset is *always* applied counter-clockwise regardless of
            the direction setting.
        """
        mapping = {
            'N': np.pi * 0.5,
            'NW': np.pi * 0.75,
            'W': np.pi,
            'SW': np.pi * 1.25,
            'S': np.pi * 1.5,
            'SE': np.pi * 1.75,
            'E': 0,
            'NE': np.pi * 0.25}
        return self.set_theta_offset(mapping[loc] + np.deg2rad(offset))
