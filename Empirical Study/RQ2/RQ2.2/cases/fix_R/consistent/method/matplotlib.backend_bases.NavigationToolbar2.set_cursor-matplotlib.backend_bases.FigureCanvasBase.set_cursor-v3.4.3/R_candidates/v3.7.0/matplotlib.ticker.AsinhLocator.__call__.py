    def __call__(self):
        vmin, vmax = self.axis.get_view_interval()
        if (vmin * vmax) < 0 and abs(1 + vmax / vmin) < self.symthresh:
            # Data-range appears to be almost symmetric, so round up:
            bound = max(abs(vmin), abs(vmax))
            return self.tick_values(-bound, bound)
        else:
            return self.tick_values(vmin, vmax)
