    def tick_values(self, vmin, vmax):
        if self.numticks == 'auto':
            if self.axis is not None:
                numticks = np.clip(self.axis.get_tick_space(), 2, 9)
            else:
                numticks = 9
        else:
            numticks = self.numticks

        b = self._base
        # dummy axis has no axes attribute
        if hasattr(self.axis, 'axes') and self.axis.axes.name == 'polar':
            vmax = math.ceil(math.log(vmax) / math.log(b))
            decades = np.arange(vmax - self.numdecs, vmax)
            ticklocs = b ** decades

            return ticklocs

        if vmin <= 0.0:
            if self.axis is not None:
                vmin = self.axis.get_minpos()

            if vmin <= 0.0 or not np.isfinite(vmin):
                raise ValueError(
                    "Data has no positive values, and therefore can not be "
                    "log-scaled.")

        vmin = math.log(vmin) / math.log(b)
        vmax = math.log(vmax) / math.log(b)

        if vmax < vmin:
            vmin, vmax = vmax, vmin

        numdec = math.floor(vmax) - math.ceil(vmin)

        if isinstance(self._subs, six.string_types):
            _first = 2.0 if self._subs == 'auto' else 1.0
            if numdec > 10 or b < 3:
                if self._subs == 'auto':
                    return np.array([])  # no minor or major ticks
                else:
                    subs = np.array([1.0])  # major ticks
            else:
                subs = np.arange(_first, b)
        else:
            subs = self._subs

        stride = 1

        if rcParams['_internal.classic_mode']:
            # Leave the bug left over from the PY2-PY3 transition.
            while numdec / stride + 1 > numticks:
                stride += 1
        else:
            while numdec // stride + 1 > numticks:
                stride += 1

        # Does subs include anything other than 1?
        have_subs = len(subs) > 1 or (len(subs == 1) and subs[0] != 1.0)

        decades = np.arange(math.floor(vmin) - stride,
                            math.ceil(vmax) + 2 * stride, stride)

        if hasattr(self, '_transform'):
            ticklocs = self._transform.inverted().transform(decades)
            if have_subs:
                if stride == 1:
                    ticklocs = np.ravel(np.outer(subs, ticklocs))
                else:
                    ticklocs = []
        else:
            if have_subs:
                ticklocs = []
                if stride == 1:
                    for decadeStart in b ** decades:
                        ticklocs.extend(subs * decadeStart)
            else:
                ticklocs = b ** decades

        return self.raise_if_exceeds(np.asarray(ticklocs))
