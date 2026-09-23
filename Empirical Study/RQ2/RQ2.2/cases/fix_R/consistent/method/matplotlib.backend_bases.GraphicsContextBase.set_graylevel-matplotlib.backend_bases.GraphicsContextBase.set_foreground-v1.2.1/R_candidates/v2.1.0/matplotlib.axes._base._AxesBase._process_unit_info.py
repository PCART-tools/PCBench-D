    def _process_unit_info(self, xdata=None, ydata=None, kwargs=None):
        """Look for unit *kwargs* and update the axis instances as necessary"""

        if self.xaxis is None or self.yaxis is None:
            return

        if xdata is not None:
            # we only need to update if there is nothing set yet.
            if not self.xaxis.have_units():
                self.xaxis.update_units(xdata)

        if ydata is not None:
            # we only need to update if there is nothing set yet.
            if not self.yaxis.have_units():
                self.yaxis.update_units(ydata)

        # process kwargs 2nd since these will override default units
        if kwargs is not None:
            xunits = kwargs.pop('xunits', self.xaxis.units)
            if self.name == 'polar':
                xunits = kwargs.pop('thetaunits', xunits)
            if xunits != self.xaxis.units:
                self.xaxis.set_units(xunits)
                # If the units being set imply a different converter,
                # we need to update.
                if xdata is not None:
                    self.xaxis.update_units(xdata)

            yunits = kwargs.pop('yunits', self.yaxis.units)
            if self.name == 'polar':
                yunits = kwargs.pop('runits', yunits)
            if yunits != self.yaxis.units:
                self.yaxis.set_units(yunits)
                # If the units being set imply a different converter,
                # we need to update.
                if ydata is not None:
                    self.yaxis.update_units(ydata)
        return kwargs
