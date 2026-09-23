    def _adjust_location(self):
        """Automatically set spine bounds to the view interval."""

        if self.spine_type == 'circle':
            return

        if self._bounds is not None:
            low, high = self._bounds
        elif self.spine_type in ('left', 'right'):
            low, high = self.axes.viewLim.intervaly
        elif self.spine_type in ('top', 'bottom'):
            low, high = self.axes.viewLim.intervalx
        else:
            raise ValueError(f'unknown spine spine_type: {self.spine_type}')

        if self._patch_type == 'arc':
            if self.spine_type in ('bottom', 'top'):
                try:
                    direction = self.axes.get_theta_direction()
                except AttributeError:
                    direction = 1
                try:
                    offset = self.axes.get_theta_offset()
                except AttributeError:
                    offset = 0
                low = low * direction + offset
                high = high * direction + offset
                if low > high:
                    low, high = high, low

                self._path = mpath.Path.arc(np.rad2deg(low), np.rad2deg(high))

                if self.spine_type == 'bottom':
                    rmin, rmax = self.axes.viewLim.intervaly
                    try:
                        rorigin = self.axes.get_rorigin()
                    except AttributeError:
                        rorigin = rmin
                    scaled_diameter = (rmin - rorigin) / (rmax - rorigin)
                    self._height = scaled_diameter
                    self._width = scaled_diameter

            else:
                raise ValueError('unable to set bounds for spine "%s"' %
                                 self.spine_type)
        else:
            v1 = self._path.vertices
            assert v1.shape == (2, 2), 'unexpected vertices shape'
            if self.spine_type in ['left', 'right']:
                v1[0, 1] = low
                v1[1, 1] = high
            elif self.spine_type in ['bottom', 'top']:
                v1[0, 0] = low
                v1[1, 0] = high
            else:
                raise ValueError('unable to set bounds for spine "%s"' %
                                 self.spine_type)
