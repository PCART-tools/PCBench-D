    def tick_values(self, vmin, vmax):
        # dummy axis has no axes attribute
        if hasattr(self.axis, 'axes') and self.axis.axes.name == 'polar':
            raise NotImplementedError('Polar axis cannot be logit scaled yet')

        vmin, vmax = self.nonsingular(vmin, vmax)
        vmin = np.log10(vmin / (1 - vmin))
        vmax = np.log10(vmax / (1 - vmax))

        decade_min = np.floor(vmin)
        decade_max = np.ceil(vmax)

        # major ticks
        if not self.minor:
            ticklocs = []
            if (decade_min <= -1):
                expo = np.arange(decade_min, min(0, decade_max + 1))
                ticklocs.extend(list(10**expo))
            if (decade_min <= 0) and (decade_max >= 0):
                ticklocs.append(0.5)
            if (decade_max >= 1):
                expo = -np.arange(max(1, decade_min), decade_max + 1)
                ticklocs.extend(list(1 - 10**expo))

        # minor ticks
        else:
            ticklocs = []
            if (decade_min <= -2):
                expo = np.arange(decade_min, min(-1, decade_max))
                newticks = np.outer(np.arange(2, 10), 10**expo).ravel()
                ticklocs.extend(list(newticks))
            if (decade_min <= 0) and (decade_max >= 0):
                ticklocs.extend([0.2, 0.3, 0.4, 0.6, 0.7, 0.8])
            if (decade_max >= 2):
                expo = -np.arange(max(2, decade_min), decade_max + 1)
                newticks = 1 - np.outer(np.arange(2, 10), 10**expo).ravel()
                ticklocs.extend(list(newticks))

        return self.raise_if_exceeds(np.array(ticklocs))
