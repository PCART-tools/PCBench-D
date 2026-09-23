    def update_from(self, other):
        """Copy properties from other to self."""
        Artist.update_from(self, other)
        self._linestyle = other._linestyle
        self._linewidth = other._linewidth
        self._color = other._color
        self._markersize = other._markersize
        self._markerfacecolor = other._markerfacecolor
        self._markerfacecoloralt = other._markerfacecoloralt
        self._markeredgecolor = other._markeredgecolor
        self._markeredgewidth = other._markeredgewidth
        self._dashSeq = other._dashSeq
        self._us_dashSeq = other._us_dashSeq
        self._dashOffset = other._dashOffset
        self._us_dashOffset = other._us_dashOffset
        self._dashcapstyle = other._dashcapstyle
        self._dashjoinstyle = other._dashjoinstyle
        self._solidcapstyle = other._solidcapstyle
        self._solidjoinstyle = other._solidjoinstyle

        self._linestyle = other._linestyle
        self._marker = MarkerStyle(other._marker.get_marker(),
                                   other._marker.get_fillstyle())
        self._drawstyle = other._drawstyle
