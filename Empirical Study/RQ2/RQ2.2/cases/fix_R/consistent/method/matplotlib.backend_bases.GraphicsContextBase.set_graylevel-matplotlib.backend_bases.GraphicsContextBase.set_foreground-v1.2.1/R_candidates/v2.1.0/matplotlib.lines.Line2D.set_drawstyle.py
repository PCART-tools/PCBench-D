    def set_drawstyle(self, drawstyle):
        """
        Set the drawstyle of the plot

        'default' connects the points with lines. The steps variants
        produce step-plots. 'steps' is equivalent to 'steps-pre' and
        is maintained for backward-compatibility.

        ACCEPTS: ['default' | 'steps' | 'steps-pre' | 'steps-mid' |
                  'steps-post']
        """
        if drawstyle is None:
            drawstyle = 'default'
        if drawstyle not in self.drawStyles:
            raise ValueError('Unrecognized drawstyle {!r}'.format(drawstyle))
        if self._drawstyle != drawstyle:
            self.stale = True
        self._drawstyle = drawstyle
