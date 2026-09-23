    def new_gc(self):
        # docstring inherited
        self.gc.ctx.save()
        # FIXME: The following doesn't properly implement a stack-like behavior
        # and relies instead on the (non-guaranteed) fact that artists never
        # rely on nesting gc states, so directly resetting the attributes (IOW
        # a single-level stack) is enough.
        self.gc._alpha = 1
        self.gc._forced_alpha = False  # if True, _alpha overrides A from RGBA
        self.gc._hatch = None
        return self.gc
