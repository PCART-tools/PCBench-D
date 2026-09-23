    def get_sizes(self, legend, orig_handle,
                  xdescent, ydescent, width, height, fontsize):
        if self._sizes is None:
            handle_sizes = orig_handle.get_sizes()
            if not len(handle_sizes):
                handle_sizes = [1]
            size_max = max(handle_sizes) * legend.markerscale ** 2
            size_min = min(handle_sizes) * legend.markerscale ** 2

            numpoints = self.get_numpoints(legend)
            if numpoints < 4:
                sizes = [.5 * (size_max + size_min), size_max,
                         size_min][:numpoints]
            else:
                rng = (size_max - size_min)
                sizes = rng * np.linspace(0, 1, numpoints) + size_min
        else:
            sizes = self._sizes

        return sizes
