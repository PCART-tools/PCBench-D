    def _adjust_location(self):
        """automatically set spine bounds to the view interval"""

        if self.spine_type == 'circle':
            return

        if self._bounds is None:
            if self.spine_type in ('left', 'right'):
                low, high = self.axes.viewLim.intervaly
            elif self.spine_type in ('top', 'bottom'):
                low, high = self.axes.viewLim.intervalx
            else:
                raise ValueError('unknown spine spine_type: %s' %
                                 self.spine_type)

            if self._smart_bounds:
                # attempt to set bounds in sophisticated way

                # handle inverted limits
                viewlim_low, viewlim_high = sorted([low, high])

                if self.spine_type in ('left', 'right'):
                    datalim_low, datalim_high = self.axes.dataLim.intervaly
                    ticks = self.axes.get_yticks()
                elif self.spine_type in ('top', 'bottom'):
                    datalim_low, datalim_high = self.axes.dataLim.intervalx
                    ticks = self.axes.get_xticks()
                # handle inverted limits
                ticks = np.sort(ticks)
                datalim_low, datalim_high = sorted([datalim_low, datalim_high])

                if datalim_low < viewlim_low:
                    # Data extends past view. Clip line to view.
                    low = viewlim_low
                else:
                    # Data ends before view ends.
                    cond = (ticks <= datalim_low) & (ticks >= viewlim_low)
                    tickvals = ticks[cond]
                    if len(tickvals):
                        # A tick is less than or equal to lowest data point.
                        low = tickvals[-1]
                    else:
                        # No tick is available
                        low = datalim_low
                    low = max(low, viewlim_low)

                if datalim_high > viewlim_high:
                    # Data extends past view. Clip line to view.
                    high = viewlim_high
                else:
                    # Data ends before view ends.
                    cond = (ticks >= datalim_high) & (ticks <= viewlim_high)
                    tickvals = ticks[cond]
                    if len(tickvals):
                        # A tick is greater than or equal to highest data
                        # point.
                        high = tickvals[0]
                    else:
                        # No tick is available
                        high = datalim_high
                    high = min(high, viewlim_high)

        else:
            low, high = self._bounds

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
