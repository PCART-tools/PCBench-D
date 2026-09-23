    def _raw_ticks(self, vmin, vmax):
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
        raw_step = (vmax - vmin) / nbins
        steps = self._extended_steps * scale
        if self._integer:
            # For steps > 1, keep only integer values.
            igood = (steps < 1) | (np.abs(steps - np.round(steps)) < 0.001)
            steps = steps[igood]

        istep = np.nonzero(steps >= raw_step)[0][0]

        # Classic round_numbers mode may require a larger step.
        if rcParams['axes.autolimit_mode'] == 'round_numbers':
            for istep in range(istep, len(steps)):
                step = steps[istep]
                best_vmin = (_vmin // step) * step
                best_vmax = best_vmin + step * nbins
                if (best_vmax >= _vmax):
                    break

        # This is an upper limit; move to smaller steps if necessary.
        for i in range(istep):
            step = steps[istep - i]
            if (self._integer and
                    np.floor(_vmax) - np.ceil(_vmin) >= self._min_n_ticks - 1):
                step = max(1, step)
            best_vmin = (_vmin // step) * step

            low = np.round(Base(step).le(_vmin - best_vmin) / step)
            high = np.round(Base(step).ge(_vmax - best_vmin) / step)
            ticks = np.arange(low, high + 1) * step + best_vmin + offset
            nticks = ((ticks <= vmax) & (ticks >= vmin)).sum()
            if nticks >= self._min_n_ticks:
                break
        return ticks
