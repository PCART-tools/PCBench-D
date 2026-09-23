    def _draw_disabled(self):
        """
        Context manager to temporary disable drawing.

        This is used for getting the drawn size of Artists.  This lets us
        run the draw process to update any Python state but does not pay the
        cost of the draw_XYZ calls on the canvas.
        """
        no_ops = {
            meth_name: lambda *args, **kwargs: None
            for meth_name in dir(RendererBase)
            if (meth_name.startswith("draw_")
                or meth_name in ["open_group", "close_group"])
        }

        return _setattr_cm(self, **no_ops)
