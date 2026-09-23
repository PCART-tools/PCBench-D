    @property
    def _constructor_expanddim(self):
        """Used when a manipulation result has one higher dimension as the
        original, such as Series.to_frame() and DataFrame.to_panel()
        """
        raise NotImplementedError
