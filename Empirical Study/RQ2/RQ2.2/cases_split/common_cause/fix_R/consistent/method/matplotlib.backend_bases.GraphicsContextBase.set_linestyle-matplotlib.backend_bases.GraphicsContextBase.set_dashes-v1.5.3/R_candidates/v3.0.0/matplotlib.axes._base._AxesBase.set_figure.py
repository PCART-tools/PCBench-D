    def set_figure(self, fig):
        """
        Set the `.Figure` for this `.Axes`.

        Parameters
        ----------
        fig : `.Figure`
        """
        martist.Artist.set_figure(self, fig)

        self.bbox = mtransforms.TransformedBbox(self._position,
                                                fig.transFigure)
        # these will be updated later as data is added
        self.dataLim = mtransforms.Bbox.null()
        self.viewLim = mtransforms.Bbox.unit()
        self.transScale = mtransforms.TransformWrapper(
            mtransforms.IdentityTransform())

        self._set_lim_and_transforms()
