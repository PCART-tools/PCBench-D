    def _set_view(self, view):
        # docstring inherited
        # An interactive view for a colorbar is the norm's vmin/vmax
        self.norm.vmin, self.norm.vmax = view
