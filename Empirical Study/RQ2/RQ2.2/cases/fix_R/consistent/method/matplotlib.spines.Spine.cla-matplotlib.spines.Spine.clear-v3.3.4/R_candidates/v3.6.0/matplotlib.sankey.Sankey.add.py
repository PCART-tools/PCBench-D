    @_docstring.dedent_interpd
    def add(self, patchlabel='', flows=None, orientations=None, labels='',
            trunklength=1.0, pathlengths=0.25, prior=None, connect=(0, 0),
            rotation=0, **kwargs):
        """
        Add a simple Sankey diagram with flows at the same hierarchical level.

        Parameters
        ----------
        patchlabel : str
            Label to be placed at the center of the diagram.
            Note that *label* (not *patchlabel*) can be passed as keyword
            argument to create an entry in the legend.

        flows : list of float
            Array of flow values.  By convention, inputs are positive and
            outputs are negative.

            Flows are placed along the top of the diagram from the inside out
            in order of their index within *flows*.  They are placed along the
            sides of the diagram from the top down and along the bottom from
            the outside in.

            If the sum of the inputs and outputs is
            nonzero, the discrepancy will appear as a cubic Bezier curve along
            the top and bottom edges of the trunk.

        orientations : list of {-1, 0, 1}
            List of orientations of the flows (or a single orientation to be
            used for all flows).  Valid values are 0 (inputs from
            the left, outputs to the right), 1 (from and to the top) or -1
            (from and to the bottom).

        labels : list of (str or None)
            List of labels for the flows (or a single label to be used for all
            flows).  Each label may be *None* (no label), or a labeling string.
            If an entry is a (possibly empty) string, then the quantity for the
            corresponding flow will be shown below the string.  However, if
            the *unit* of the main diagram is None, then quantities are never
            shown, regardless of the value of this argument.

        trunklength : float
            Length between the bases of the input and output groups (in
            data-space units).

        pathlengths : list of float
            List of lengths of the vertical arrows before break-in or after
            break-away.  If a single value is given, then it will be applied to
            the first (inside) paths on the top and bottom, and the length of
            all other arrows will be justified accordingly.  The *pathlengths*
            are not applied to the horizontal inputs and outputs.

        prior : int
            Index of the prior diagram to which this diagram should be
            connected.

        connect : (int, int)
            A (prior, this) tuple indexing the flow of the prior diagram and
            the flow of this diagram which should be connected.  If this is the
            first diagram or *prior* is *None*, *connect* will be ignored.

        rotation : float
            Angle of rotation of the diagram in degrees.  The interpretation of
            the *orientations* argument will be rotated accordingly (e.g., if
            *rotation* == 90, an *orientations* entry of 1 means to/from the
            left).  *rotation* is ignored if this diagram is connected to an
            existing one (using *prior* and *connect*).

        Returns
        -------
        Sankey
            The current `.Sankey` instance.

        Other Parameters
        ----------------
        **kwargs
           Additional keyword arguments set `matplotlib.patches.PathPatch`
           properties, listed below.  For example, one may want to use
           ``fill=False`` or ``label="A legend entry"``.

        %(Patch:kwdoc)s

        See Also
        --------
        Sankey.finish
        """
        # Check and preprocess the arguments.
        if flows is None:
            flows = np.array([1.0, -1.0])
        else:
            flows = np.array(flows)
        n = flows.shape[0]  # Number of flows
        if rotation is None:
            rotation = 0
        else:
            # In the code below, angles are expressed in deg/90.
            rotation /= 90.0
        if orientations is None:
            orientations = 0
        try:
            orientations = np.broadcast_to(orientations, n)
        except ValueError:
            raise ValueError(
                f"The shapes of 'flows' {np.shape(flows)} and 'orientations' "
                f"{np.shape(orientations)} are incompatible"
            ) from None
        try:
            labels = np.broadcast_to(labels, n)
        except ValueError:
            raise ValueError(
                f"The shapes of 'flows' {np.shape(flows)} and 'labels' "
                f"{np.shape(labels)} are incompatible"
            ) from None
        if trunklength < 0:
            raise ValueError(
                "'trunklength' is negative, which is not allowed because it "
                "would cause poor layout")
        if abs(np.sum(flows)) > self.tolerance:
            _log.info("The sum of the flows is nonzero (%f; patchlabel=%r); "
                      "is the system not at steady state?",
                      np.sum(flows), patchlabel)
        scaled_flows = self.scale * flows
        gain = sum(max(flow, 0) for flow in scaled_flows)
        loss = sum(min(flow, 0) for flow in scaled_flows)
        if prior is not None:
            if prior < 0:
                raise ValueError("The index of the prior diagram is negative")
            if min(connect) < 0:
                raise ValueError(
                    "At least one of the connection indices is negative")
            if prior >= len(self.diagrams):
                raise ValueError(
                    f"The index of the prior diagram is {prior}, but there "
                    f"are only {len(self.diagrams)} other diagrams")
            if connect[0] >= len(self.diagrams[prior].flows):
                raise ValueError(
                    "The connection index to the source diagram is {}, but "
                    "that diagram has only {} flows".format(
                        connect[0], len(self.diagrams[prior].flows)))
            if connect[1] >= n:
                raise ValueError(
                    f"The connection index to this diagram is {connect[1]}, "
                    f"but this diagram has only {n} flows")
            if self.diagrams[prior].angles[connect[0]] is None:
                raise ValueError(
                    f"The connection cannot be made, which may occur if the "
                    f"magnitude of flow {connect[0]} of diagram {prior} is "
                    f"less than the specified tolerance")
            flow_error = (self.diagrams[prior].flows[connect[0]] +
                          flows[connect[1]])
            if abs(flow_error) >= self.tolerance:
                raise ValueError(
                    f"The scaled sum of the connected flows is {flow_error}, "
                    f"which is not within the tolerance ({self.tolerance})")

        # Determine if the flows are inputs.
        are_inputs = [None] * n
        for i, flow in enumerate(flows):
            if flow >= self.tolerance:
                are_inputs[i] = True
            elif flow <= -self.tolerance:
                are_inputs[i] = False
            else:
                _log.info(
                    "The magnitude of flow %d (%f) is below the tolerance "
                    "(%f).\nIt will not be shown, and it cannot be used in a "
                    "connection.", i, flow, self.tolerance)

        # Determine the angles of the arrows (before rotation).
        angles = [None] * n
        for i, (orient, is_input) in enumerate(zip(orientations, are_inputs)):
            if orient == 1:
                if is_input:
                    angles[i] = DOWN
                elif is_input is False:
                    # Be specific since is_input can be None.
                    angles[i] = UP
            elif orient == 0:
                if is_input is not None:
                    angles[i] = RIGHT
            else:
                if orient != -1:
                    raise ValueError(
                        f"The value of orientations[{i}] is {orient}, "
                        f"but it must be -1, 0, or 1")
                if is_input:
                    angles[i] = UP
                elif is_input is False:
                    angles[i] = DOWN

        # Justify the lengths of the paths.
        if np.iterable(pathlengths):
            if len(pathlengths) != n:
                raise ValueError(
                    f"The lengths of 'flows' ({n}) and 'pathlengths' "
                    f"({len(pathlengths)}) are incompatible")
        else:  # Make pathlengths into a list.
            urlength = pathlengths
            ullength = pathlengths
            lrlength = pathlengths
            lllength = pathlengths
            d = dict(RIGHT=pathlengths)
            pathlengths = [d.get(angle, 0) for angle in angles]
            # Determine the lengths of the top-side arrows
            # from the middle outwards.
            for i, (angle, is_input, flow) in enumerate(zip(angles, are_inputs,
                                                            scaled_flows)):
                if angle == DOWN and is_input:
                    pathlengths[i] = ullength
                    ullength += flow
                elif angle == UP and is_input is False:
                    pathlengths[i] = urlength
                    urlength -= flow  # Flow is negative for outputs.
            # Determine the lengths of the bottom-side arrows
            # from the middle outwards.
            for i, (angle, is_input, flow) in enumerate(reversed(list(zip(
                  angles, are_inputs, scaled_flows)))):
                if angle == UP and is_input:
                    pathlengths[n - i - 1] = lllength
                    lllength += flow
                elif angle == DOWN and is_input is False:
                    pathlengths[n - i - 1] = lrlength
                    lrlength -= flow
            # Determine the lengths of the left-side arrows
            # from the bottom upwards.
            has_left_input = False
            for i, (angle, is_input, spec) in enumerate(reversed(list(zip(
                  angles, are_inputs, zip(scaled_flows, pathlengths))))):
                if angle == RIGHT:
                    if is_input:
                        if has_left_input:
                            pathlengths[n - i - 1] = 0
                        else:
                            has_left_input = True
            # Determine the lengths of the right-side arrows
            # from the top downwards.
            has_right_output = False
            for i, (angle, is_input, spec) in enumerate(zip(
                  angles, are_inputs, list(zip(scaled_flows, pathlengths)))):
                if angle == RIGHT:
                    if is_input is False:
                        if has_right_output:
                            pathlengths[i] = 0
                        else:
                            has_right_output = True

        # Begin the subpaths, and smooth the transition if the sum of the flows
        # is nonzero.
        urpath = [(Path.MOVETO, [(self.gap - trunklength / 2.0),  # Upper right
                                 gain / 2.0]),
                  (Path.LINETO, [(self.gap - trunklength / 2.0) / 2.0,
                                 gain / 2.0]),
                  (Path.CURVE4, [(self.gap - trunklength / 2.0) / 8.0,
                                 gain / 2.0]),
                  (Path.CURVE4, [(trunklength / 2.0 - self.gap) / 8.0,
                                 -loss / 2.0]),
                  (Path.LINETO, [(trunklength / 2.0 - self.gap) / 2.0,
                                 -loss / 2.0]),
                  (Path.LINETO, [(trunklength / 2.0 - self.gap),
                                 -loss / 2.0])]
        llpath = [(Path.LINETO, [(trunklength / 2.0 - self.gap),  # Lower left
                                 loss / 2.0]),
                  (Path.LINETO, [(trunklength / 2.0 - self.gap) / 2.0,
                                 loss / 2.0]),
                  (Path.CURVE4, [(trunklength / 2.0 - self.gap) / 8.0,
                                 loss / 2.0]),
                  (Path.CURVE4, [(self.gap - trunklength / 2.0) / 8.0,
                                 -gain / 2.0]),
                  (Path.LINETO, [(self.gap - trunklength / 2.0) / 2.0,
                                 -gain / 2.0]),
                  (Path.LINETO, [(self.gap - trunklength / 2.0),
                                 -gain / 2.0])]
        lrpath = [(Path.LINETO, [(trunklength / 2.0 - self.gap),  # Lower right
                                 loss / 2.0])]
        ulpath = [(Path.LINETO, [self.gap - trunklength / 2.0,  # Upper left
                                 gain / 2.0])]

        # Add the subpaths and assign the locations of the tips and labels.
        tips = np.zeros((n, 2))
        label_locations = np.zeros((n, 2))
        # Add the top-side inputs and outputs from the middle outwards.
        for i, (angle, is_input, spec) in enumerate(zip(
              angles, are_inputs, list(zip(scaled_flows, pathlengths)))):
            if angle == DOWN and is_input:
                tips[i, :], label_locations[i, :] = self._add_input(
                    ulpath, angle, *spec)
            elif angle == UP and is_input is False:
                tips[i, :], label_locations[i, :] = self._add_output(
                    urpath, angle, *spec)
        # Add the bottom-side inputs and outputs from the middle outwards.
        for i, (angle, is_input, spec) in enumerate(reversed(list(zip(
              angles, are_inputs, list(zip(scaled_flows, pathlengths)))))):
            if angle == UP and is_input:
                tip, label_location = self._add_input(llpath, angle, *spec)
                tips[n - i - 1, :] = tip
                label_locations[n - i - 1, :] = label_location
            elif angle == DOWN and is_input is False:
                tip, label_location = self._add_output(lrpath, angle, *spec)
                tips[n - i - 1, :] = tip
                label_locations[n - i - 1, :] = label_location
        # Add the left-side inputs from the bottom upwards.
        has_left_input = False
        for i, (angle, is_input, spec) in enumerate(reversed(list(zip(
              angles, are_inputs, list(zip(scaled_flows, pathlengths)))))):
            if angle == RIGHT and is_input:
                if not has_left_input:
                    # Make sure the lower path extends
                    # at least as far as the upper one.
                    if llpath[-1][1][0] > ulpath[-1][1][0]:
                        llpath.append((Path.LINETO, [ulpath[-1][1][0],
                                                     llpath[-1][1][1]]))
                    has_left_input = True
                tip, label_location = self._add_input(llpath, angle, *spec)
                tips[n - i - 1, :] = tip
                label_locations[n - i - 1, :] = label_location
        # Add the right-side outputs from the top downwards.
        has_right_output = False
        for i, (angle, is_input, spec) in enumerate(zip(
              angles, are_inputs, list(zip(scaled_flows, pathlengths)))):
            if angle == RIGHT and is_input is False:
                if not has_right_output:
                    # Make sure the upper path extends
                    # at least as far as the lower one.
                    if urpath[-1][1][0] < lrpath[-1][1][0]:
                        urpath.append((Path.LINETO, [lrpath[-1][1][0],
                                                     urpath[-1][1][1]]))
                    has_right_output = True
                tips[i, :], label_locations[i, :] = self._add_output(
                    urpath, angle, *spec)
        # Trim any hanging vertices.
        if not has_left_input:
            ulpath.pop()
            llpath.pop()
        if not has_right_output:
            lrpath.pop()
            urpath.pop()

        # Concatenate the subpaths in the correct order (clockwise from top).
        path = (urpath + self._revert(lrpath) + llpath + self._revert(ulpath) +
                [(Path.CLOSEPOLY, urpath[0][1])])

        # Create a patch with the Sankey outline.
        codes, vertices = zip(*path)
        vertices = np.array(vertices)

        def _get_angle(a, r):
            if a is None:
                return None
            else:
                return a + r

        if prior is None:
            if rotation != 0:  # By default, none of this is needed.
                angles = [_get_angle(angle, rotation) for angle in angles]
                rotate = Affine2D().rotate_deg(rotation * 90).transform_affine
                tips = rotate(tips)
                label_locations = rotate(label_locations)
                vertices = rotate(vertices)
            text = self.ax.text(0, 0, s=patchlabel, ha='center', va='center')
        else:
            rotation = (self.diagrams[prior].angles[connect[0]] -
                        angles[connect[1]])
            angles = [_get_angle(angle, rotation) for angle in angles]
            rotate = Affine2D().rotate_deg(rotation * 90).transform_affine
            tips = rotate(tips)
            offset = self.diagrams[prior].tips[connect[0]] - tips[connect[1]]
            translate = Affine2D().translate(*offset).transform_affine
            tips = translate(tips)
            label_locations = translate(rotate(label_locations))
            vertices = translate(rotate(vertices))
            kwds = dict(s=patchlabel, ha='center', va='center')
            text = self.ax.text(*offset, **kwds)
        if mpl.rcParams['_internal.classic_mode']:
            fc = kwargs.pop('fc', kwargs.pop('facecolor', '#bfd1d4'))
            lw = kwargs.pop('lw', kwargs.pop('linewidth', 0.5))
        else:
            fc = kwargs.pop('fc', kwargs.pop('facecolor', None))
            lw = kwargs.pop('lw', kwargs.pop('linewidth', None))
        if fc is None:
            fc = next(self.ax._get_patches_for_fill.prop_cycler)['color']
        patch = PathPatch(Path(vertices, codes), fc=fc, lw=lw, **kwargs)
        self.ax.add_patch(patch)

        # Add the path labels.
        texts = []
        for number, angle, label, location in zip(flows, angles, labels,
                                                  label_locations):
            if label is None or angle is None:
                label = ''
            elif self.unit is not None:
                if isinstance(self.format, str):
                    quantity = self.format % abs(number) + self.unit
                elif callable(self.format):
                    quantity = self.format(number)
                else:
                    raise TypeError(
                        'format must be callable or a format string')
                if label != '':
                    label += "\n"
                label += quantity
            texts.append(self.ax.text(x=location[0], y=location[1],
                                      s=label,
                                      ha='center', va='center'))
        # Text objects are placed even they are empty (as long as the magnitude
        # of the corresponding flow is larger than the tolerance) in case the
        # user wants to provide labels later.

        # Expand the size of the diagram if necessary.
        self.extent = (min(np.min(vertices[:, 0]),
                           np.min(label_locations[:, 0]),
                           self.extent[0]),
                       max(np.max(vertices[:, 0]),
                           np.max(label_locations[:, 0]),
                           self.extent[1]),
                       min(np.min(vertices[:, 1]),
                           np.min(label_locations[:, 1]),
                           self.extent[2]),
                       max(np.max(vertices[:, 1]),
                           np.max(label_locations[:, 1]),
                           self.extent[3]))
        # Include both vertices _and_ label locations in the extents; there are
        # where either could determine the margins (e.g., arrow shoulders).

        # Add this diagram as a subdiagram.
        self.diagrams.append(
            SimpleNamespace(patch=patch, flows=flows, angles=angles, tips=tips,
                            text=text, texts=texts))

        # Allow a daisy-chained call structure (see docstring for the class).
        return self
