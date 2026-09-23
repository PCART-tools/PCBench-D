    def _process_colors(self):
        """
        Color argument processing for contouring.

        Note that we base the color mapping on the contour levels
        and layers, not on the actual range of the Z values.  This
        means we don't have to worry about bad values in Z, and we
        always have the full dynamic range available for the selected
        levels.

        The color is based on the midpoint of the layer, except for
        extended end layers.  By default, the norm vmin and vmax
        are the extreme values of the non-extended levels.  Hence,
        the layer color extremes are not the extreme values of
        the colormap itself, but approach those values as the number
        of levels increases.  An advantage of this scheme is that
        line contours, when added to filled contours, take on
        colors that are consistent with those of the filled regions;
        for example, a contour line on the boundary between two
        regions will have a color intermediate between those
        of the regions.

        """
        self.monochrome = self.cmap.monochrome
        if self.colors is not None:
            # Generate integers for direct indexing.
            i0, i1 = 0, len(self.levels)
            if self.filled:
                i1 -= 1
                # Out of range indices for over and under:
                if self.extend in ('both', 'min'):
                    i0 -= 1
                if self.extend in ('both', 'max'):
                    i1 += 1
            self.cvalues = list(range(i0, i1))
            self.set_norm(colors.NoNorm())
        else:
            self.cvalues = self.layers
        self.set_array(self.levels)
        self.autoscale_None()
        if self.extend in ('both', 'max', 'min'):
            self.norm.clip = False
