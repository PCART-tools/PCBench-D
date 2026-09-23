    def tick_values(self, vmin, vmax):
        # Construct a set of uniformly-spaced "on-screen" locations.
        ymin, ymax = self.linear_width * np.arcsinh(np.array([vmin, vmax])
                                                    / self.linear_width)
        ys = np.linspace(ymin, ymax, self.numticks)
        zero_dev = abs(ys / (ymax - ymin))
        if ymin * ymax < 0:
            # Ensure that the zero tick-mark is included, if the axis straddles zero.
            ys = np.hstack([ys[(zero_dev > 0.5 / self.numticks)], 0.0])

        # Transform the "on-screen" grid to the data space:
        xs = self.linear_width * np.sinh(ys / self.linear_width)
        zero_xs = (ys == 0)

        # Round the data-space values to be intuitive base-n numbers, keeping track of
        # positive and negative values separately and carefully treating the zero value.
        with np.errstate(divide="ignore"):  # base ** log(0) = base ** -inf = 0.
            if self.base > 1:
                pows = (np.sign(xs)
                        * self.base ** np.floor(np.log(abs(xs)) / math.log(self.base)))
                qs = np.outer(pows, self.subs).flatten() if self.subs else pows
            else:  # No need to adjust sign(pows), as it cancels out when computing qs.
                pows = np.where(zero_xs, 1, 10**np.floor(np.log10(abs(xs))))
                qs = pows * np.round(xs / pows)
        ticks = np.array(sorted(set(qs)))

        return ticks if len(ticks) >= 2 else np.linspace(vmin, vmax, self.numticks)
