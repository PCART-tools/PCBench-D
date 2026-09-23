    def set_linestyle(self, style):
        """
        Set the linestyle to be one of ('solid', 'dashed', 'dashdot',
        'dotted'). One may specify customized dash styles by providing
        a tuple of (offset, dash pairs). For example, the predefiend
        linestyles have following values.:

         'dashed'  : (0, (6.0, 6.0)),
         'dashdot' : (0, (3.0, 5.0, 1.0, 5.0)),
         'dotted'  : (0, (1.0, 3.0)),
        """

        if style in self.dashd:
            offset, dashes = self.dashd[style]
        elif isinstance(style, tuple):
            offset, dashes = style
        else:
            raise ValueError('Unrecognized linestyle: %s' % str(style))

        self._linestyle = style
        self.set_dashes(offset, dashes)
