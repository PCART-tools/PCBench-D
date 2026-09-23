    def resize(self, w, h):
        """
        UNUSED: Set the canvas size in pixels.

        Certain backends may implement a similar method internally, but this is
        not a requirement of, nor is it used by, Matplotlib itself.
        """
        # The entire method is actually deprecated, but we allow pass-through
        # to a parent class to support e.g. QWidget.resize.
        if hasattr(super(), "resize"):
            return super().resize(w, h)
        else:
            _api.warn_deprecated("3.6", name="resize", obj_type="method",
                                 alternative="FigureManagerBase.resize")
