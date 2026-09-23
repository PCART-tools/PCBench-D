    def grab_frame(self, **savefig_kwargs):
        from matplotlib.animation import _validate_grabframe_kwargs
        _validate_grabframe_kwargs(savefig_kwargs)
        self.savefig_kwargs = savefig_kwargs
        self._count += 1
