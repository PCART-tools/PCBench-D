    @toolbar.setter
    def toolbar(self, value):
        # Never allow this, except that base class inits this to None before
        # the frame is set up.
        if value is not None or hasattr(self, "frame"):
            raise AttributeError("can't set attribute")
