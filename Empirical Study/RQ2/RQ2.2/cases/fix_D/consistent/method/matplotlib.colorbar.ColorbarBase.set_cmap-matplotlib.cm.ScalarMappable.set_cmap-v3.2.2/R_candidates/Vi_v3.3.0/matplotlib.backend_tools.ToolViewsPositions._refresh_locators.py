    def _refresh_locators(self):
        for a in self.figure.get_axes():
            xaxis = getattr(a, 'xaxis', None)
            yaxis = getattr(a, 'yaxis', None)
            zaxis = getattr(a, 'zaxis', None)
            locators = []
            if xaxis is not None:
                locators.append(xaxis.get_major_locator())
                locators.append(xaxis.get_minor_locator())
            if yaxis is not None:
                locators.append(yaxis.get_major_locator())
                locators.append(yaxis.get_minor_locator())
            if zaxis is not None:
                locators.append(zaxis.get_major_locator())
                locators.append(zaxis.get_minor_locator())

            for loc in locators:
                mpl.ticker._if_refresh_overridden_call_and_emit_deprec(loc)
        self.figure.canvas.draw_idle()
