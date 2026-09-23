    @property
    def lut(self):
        """
        For external access to the lut, i.e. for displaying the cmap.
        For circular colormaps this returns a lut with a circular mask.

        Internal functions (such as to_rgb()) should use _lut
        which stores the lut without a circular mask
        A lut without the circular mask is needed in to_rgb() because the
        conversion from floats to ints results in some some pixel-requests
        just outside of the circular mask

        """
        if not self._isinit:
            self._init()
        lut = np.copy(self._lut)
        if self.shape == 'circle' or self.shape == 'circleignore':
            n = np.linspace(-1, 1, self.N)
            m = np.linspace(-1, 1, self.M)
            radii_sqr = (n**2)[:, np.newaxis] + (m**2)[np.newaxis, :]
            mask_outside = radii_sqr > 1
            lut[mask_outside, 3] = 0
        return lut
