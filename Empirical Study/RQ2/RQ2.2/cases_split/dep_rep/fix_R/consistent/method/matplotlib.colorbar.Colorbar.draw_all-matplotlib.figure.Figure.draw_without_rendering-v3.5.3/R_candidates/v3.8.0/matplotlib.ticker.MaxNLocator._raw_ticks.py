    def _raw_ticks(self, vmin, vmax):
        """
        Generate a list of tick locations including the range *vmin* to
        *vmax*.  In some applications, one or both of the end locations
        will not be needed, in which case they are trimmed off
        elsewhere.
        """
        if self._nbins == 'auto':
            if self.axis is not None:
                nbins = np.clip(self.axis.get_tick_space(),
                                max(1, self._min_n_ticks - 1), 9)
            else:
                nbins = 9
        else:
            nbins = self._nbins

        scale, offset = scale_range(vmin, vmax, nbins)
        _vmin = vmin - offset
        _vmax = vmax - offset
        steps = self._extended_steps * scale
        if self._integer:
            # For steps > 1, keep only integer values.
            igood = (steps < 1) | (np.abs(steps - np.round(steps)) < 0.001)
            steps = steps[igood]

        raw_step = ((_vmax - _vmin) / nbins)
        large_steps = steps >= raw_step
        if mpl.rcParams['axes.autolimit_mode'] == 'round_numbers':
            # Classic round_numbers mode may require a larger step.
            # Get first multiple of steps that are <= _vmin
            floored_vmins = (_vmin // steps) * steps
            floored_vmaxs = floored_vmins + steps * nbins
            large_steps = large_steps & (floored_vmaxs >= _vmax)

        # Find index of smallest large step
        istep = np.nonzero(large_steps)[0][0]

        # Start at smallest of the steps greater than the raw step, and check
        # if it provides enough ticks. If not, work backwards through
        # smaller steps until one is found that provides enough ticks.
        for step in steps[:istep+1][::-1]:

            if (self._integer and
                    np.floor(_vmax) - np.ceil(_vmin) >= self._min_n_ticks - 1):
                step = max(1, step)
            best_vmin = (_vmin // step) * step

            # Find tick locations spanning the vmin-vmax range, taking into
            # account degradation of precision when there is a large offset.
            # The edge ticks beyond vmin and/or vmax are needed for the
            # "round_numbers" autolimit mode.
            edge = _Edge_integer(step, offset)
            low = edge.le(_vmin - best_vmin)
            high = edge.ge(_vmax - best_vmin)
            ticks = np.arange(low, high + 1) * step + best_vmin
            # Count only the ticks that will be displayed.
            nticks = ((ticks <= _vmax) & (ticks >= _vmin)).sum()
            if nticks >= self._min_n_ticks:
                break
        return ticks + offset
