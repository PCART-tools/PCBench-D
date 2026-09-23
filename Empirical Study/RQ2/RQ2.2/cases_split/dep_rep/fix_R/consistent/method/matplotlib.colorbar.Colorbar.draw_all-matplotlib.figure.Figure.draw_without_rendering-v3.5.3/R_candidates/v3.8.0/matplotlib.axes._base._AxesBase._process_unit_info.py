    def _process_unit_info(self, datasets=None, kwargs=None, *, convert=True):
        """
        Set axis units based on *datasets* and *kwargs*, and optionally apply
        unit conversions to *datasets*.

        Parameters
        ----------
        datasets : list
            List of (axis_name, dataset) pairs (where the axis name is defined
            as in `._axis_map`).  Individual datasets can also be None
            (which gets passed through).
        kwargs : dict
            Other parameters from which unit info (i.e., the *xunits*,
            *yunits*, *zunits* (for 3D Axes), *runits* and *thetaunits* (for
            polar) entries) is popped, if present.  Note that this dict is
            mutated in-place!
        convert : bool, default: True
            Whether to return the original datasets or the converted ones.

        Returns
        -------
        list
            Either the original datasets if *convert* is False, or the
            converted ones if *convert* is True (the default).
        """
        # The API makes datasets a list of pairs rather than an axis_name to
        # dataset mapping because it is sometimes necessary to process multiple
        # datasets for a single axis, and concatenating them may be tricky
        # (e.g. if some are scalars, etc.).
        datasets = datasets or []
        kwargs = kwargs or {}
        axis_map = self._axis_map
        for axis_name, data in datasets:
            try:
                axis = axis_map[axis_name]
            except KeyError:
                raise ValueError(f"Invalid axis name: {axis_name!r}") from None
            # Update from data if axis is already set but no unit is set yet.
            if axis is not None and data is not None and not axis.have_units():
                axis.update_units(data)
        for axis_name, axis in axis_map.items():
            # Return if no axis is set.
            if axis is None:
                continue
            # Check for units in the kwargs, and if present update axis.
            units = kwargs.pop(f"{axis_name}units", axis.units)
            if self.name == "polar":
                # Special case: polar supports "thetaunits"/"runits".
                polar_units = {"x": "thetaunits", "y": "runits"}
                units = kwargs.pop(polar_units[axis_name], units)
            if units != axis.units and units is not None:
                axis.set_units(units)
                # If the units being set imply a different converter,
                # we need to update again.
                for dataset_axis_name, data in datasets:
                    if dataset_axis_name == axis_name and data is not None:
                        axis.update_units(data)
        return [axis_map[axis_name].convert_units(data)
                if convert and data is not None else data
                for axis_name, data in datasets]
