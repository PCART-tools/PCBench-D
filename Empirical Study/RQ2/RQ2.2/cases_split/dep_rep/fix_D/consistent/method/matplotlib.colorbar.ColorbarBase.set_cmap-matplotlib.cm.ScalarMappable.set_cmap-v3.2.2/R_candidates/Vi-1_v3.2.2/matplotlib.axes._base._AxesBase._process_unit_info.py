    def _process_unit_info(self, xdata=None, ydata=None, kwargs=None):
        """Look for unit *kwargs* and update the axis instances as necessary"""

        def _process_single_axis(data, axis, unit_name, kwargs):
            # Return if there's no axis set
            if axis is None:
                return kwargs

            if data is not None:
                # We only need to update if there is nothing set yet.
                if not axis.have_units():
                    axis.update_units(data)

            # Check for units in the kwargs, and if present update axis
            if kwargs is not None:
                units = kwargs.pop(unit_name, axis.units)
                if self.name == 'polar':
                    polar_units = {'xunits': 'thetaunits', 'yunits': 'runits'}
                    units = kwargs.pop(polar_units[unit_name], units)

                if units != axis.units:
                    axis.set_units(units)
                    # If the units being set imply a different converter,
                    # we need to update.
                    if data is not None:
                        axis.update_units(data)
            return kwargs

        kwargs = _process_single_axis(xdata, self.xaxis, 'xunits', kwargs)
        kwargs = _process_single_axis(ydata, self.yaxis, 'yunits', kwargs)
        return kwargs
