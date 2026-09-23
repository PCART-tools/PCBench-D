    @toolbar.setter
    def toolbar(self, value):
        # Never allow this, except that base class inits this to None before
        # the frame is set up.
        if not self._initializing:
            raise AttributeError("can't set attribute")
