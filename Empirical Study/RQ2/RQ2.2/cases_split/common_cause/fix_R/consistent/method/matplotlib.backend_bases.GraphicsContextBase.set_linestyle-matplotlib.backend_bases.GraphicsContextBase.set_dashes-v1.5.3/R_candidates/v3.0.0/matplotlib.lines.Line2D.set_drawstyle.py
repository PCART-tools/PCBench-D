    def set_drawstyle(self, drawstyle):
        """
        Set the drawstyle of the plot

        'default' connects the points with lines. The steps variants
        produce step-plots. 'steps' is equivalent to 'steps-pre' and
        is maintained for backward-compatibility.

        Parameters
        ----------
        drawstyle : {'default', 'steps', 'steps-pre', 'steps-mid', \
'steps-post'}
        """
        if drawstyle is None:
            drawstyle = 'default'
        if drawstyle not in self.drawStyles:
            raise ValueError('Unrecognized drawstyle {!r}'.format(drawstyle))
        if self._drawstyle != drawstyle:
            self.stale = True
            # invalidate to trigger a recache of the path
            self._invalidx = True
        self._drawstyle = drawstyle
