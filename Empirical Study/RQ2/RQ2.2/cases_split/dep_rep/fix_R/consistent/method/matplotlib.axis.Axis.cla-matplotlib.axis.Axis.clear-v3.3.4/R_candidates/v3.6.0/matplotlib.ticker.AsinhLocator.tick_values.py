    def tick_values(self, vmin, vmax):
        # Construct a set of "on-screen" locations
        # that are uniformly spaced:
        ymin, ymax = self.linear_width * np.arcsinh(np.array([vmin, vmax])
                                                        / self.linear_width)
        ys = np.linspace(ymin, ymax, self.numticks)
        zero_dev = np.abs(ys / (ymax - ymin))
        if (ymin * ymax) < 0:
            # Ensure that the zero tick-mark is included,
            # if the axis straddles zero
            ys = np.hstack([ys[(zero_dev > 0.5 / self.numticks)], 0.0])

        # Transform the "on-screen" grid to the data space:
        xs = self.linear_width * np.sinh(ys / self.linear_width)
        zero_xs = (ys == 0)

        # Round the data-space values to be intuitive base-n numbers,
        # keeping track of positive and negative values separately,
        # but giving careful treatment to the zero value:
        if self.base > 1:
            log_base = math.log(self.base)
            powers = (
                np.where(zero_xs, 0, np.sign(xs)) *
                np.power(self.base,
                         np.where(zero_xs, 0.0,
                                  np.floor(np.log(np.abs(xs) + zero_xs*1e-6)
                                                / log_base)))
            )
            if self.subs:
                qs = np.outer(powers, self.subs).flatten()
            else:
                qs = powers
        else:
            powers = (
                np.where(xs >= 0, 1, -1) *
                np.power(10, np.where(zero_xs, 0.0,
                                      np.floor(np.log10(np.abs(xs)
                                                        + zero_xs*1e-6))))
            )
            qs = powers * np.round(xs / powers)
        ticks = np.array(sorted(set(qs)))

        if len(ticks) >= 2:
            return ticks
        else:
            return np.linspace(vmin, vmax, self.numticks)
