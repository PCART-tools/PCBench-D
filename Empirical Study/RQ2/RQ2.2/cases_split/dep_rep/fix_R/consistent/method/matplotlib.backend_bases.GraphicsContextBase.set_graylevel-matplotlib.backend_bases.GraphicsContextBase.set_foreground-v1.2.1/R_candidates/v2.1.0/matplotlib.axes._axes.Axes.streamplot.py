    @_preprocess_data(replace_names=["x", "y", "u", "v", "start_points"],
                      label_namer=None)
    def streamplot(self, x, y, u, v, density=1, linewidth=None, color=None,
                   cmap=None, norm=None, arrowsize=1, arrowstyle='-|>',
                   minlength=0.1, transform=None, zorder=None,
                   start_points=None, maxlength=4.0,
                   integration_direction='both'):
        if not self._hold:
            self.cla()
        stream_container = mstream.streamplot(
            self, x, y, u, v,
            density=density,
            linewidth=linewidth,
            color=color,
            cmap=cmap,
            norm=norm,
            arrowsize=arrowsize,
            arrowstyle=arrowstyle,
            minlength=minlength,
            start_points=start_points,
            transform=transform,
            zorder=zorder,
            maxlength=maxlength,
            integration_direction=integration_direction)
        return stream_container
