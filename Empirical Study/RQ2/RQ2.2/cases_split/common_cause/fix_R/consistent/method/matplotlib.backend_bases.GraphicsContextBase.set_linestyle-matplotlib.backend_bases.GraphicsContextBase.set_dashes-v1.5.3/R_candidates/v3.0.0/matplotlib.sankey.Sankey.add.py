    @docstring.dedent_interpd
    def add(self, patchlabel='', flows=None, orientations=None, labels='',
            trunklength=1.0, pathlengths=0.25, prior=None, connect=(0, 0),
            rotation=0, **kwargs):
        """
        Add a simple Sankey diagram with flows at the same hierarchical level.

        Return value is the instance of :class:`Sankey`.

        Optional keyword arguments:

          ===============   ===================================================
          Keyword           Description
          ===============   ===================================================
          *patchlabel*      label to be placed at the center of the diagram
                            Note: *label* (not *patchlabel*) will be passed to
                            the patch through ``**kwargs`` and can be used to
                            create an entry in the legend.
          *flows*           array of flow values
                            By convention, inputs are positive and outputs are
                            negative.
          *orientations*    list of orientations of the paths
                            Valid values are 1 (from/to the top), 0 (from/to
                            the left or right), or -1 (from/to the bottom).  If
                            *orientations* == 0, inputs will break in from the
                            left and outputs will break away to the right.
          *labels*          list of specifications of the labels for the flows
                            Each value may be *None* (no labels), '' (just
                            label the quantities), or a labeling string.  If a
                            single value is provided, it will be applied to all
                            flows.  If an entry is a non-empty string, then the
                            quantity for the corresponding flow will be shown
                            below the string.  However, if the *unit* of the
                            main diagram is None, then quantities are never
                            shown, regardless of the value of this argument.
          *trunklength*     length between the bases of the input and output
                            groups
          *pathlengths*     list of lengths of the arrows before break-in or
                            after break-away
                            If a single value is given, then it will be applied
                            to the first (inside) paths on the top and bottom,
                            and the length of all other arrows will be
                            justified accordingly.  The *pathlengths* are not
                            applied to the horizontal inputs and outputs.
          *prior*           index of the prior diagram to which this diagram
                            should be connected
          *connect*         a (prior, this) tuple indexing the flow of the
                            prior diagram and the flow of this diagram which
                            should be connected
                            If this is the first diagram or *prior* is *None*,
                            *connect* will be ignored.
          *rotation*        angle of rotation of the diagram [deg]
                            *rotation* is ignored if this diagram is connected
                            to an existing one (using *prior* and *connect*).
                            The interpretation of the *orientations* argument
                            will be rotated accordingly (e.g., if *rotation*
                            == 90, an *orientations* entry of 1 means to/from
                            the left).
          ===============   ===================================================

        Valid kwargs are :meth:`matplotlib.patches.PathPatch` arguments:

        %(Patch)s

        As examples, ``fill=False`` and ``label='A legend entry'``.
        By default, ``facecolor='#bfd1d4'`` (light blue) and
        ``linewidth=0.5``.

        The indexing parameters (*prior* and *connect*) are zero-based.

        The flows are placed along the top of the diagram from the inside out
        in order of their index within the *flows* list or array.  They are
        placed along the sides of the diagram from the top down and along the
        bottom from the outside in.

        If the sum of the inputs and outputs is nonzero, the discrepancy
        will appear as a cubic Bezier curve along the top and bottom edges of
        the trunk.

        .. seealso::

            :meth:`finish`
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
            orientations = [0, 0]
        if len(orientations) != n:
            raise ValueError(
            "orientations and flows must have the same length.\n"
            "orientations has length %d, but flows has length %d."
            % (len(orientations), n))
        if labels != '' and getattr(labels, '__iter__', False):
            # iterable() isn't used because it would give True if labels is a
            # string
            if len(labels) != n:
                raise ValueError(
                "If labels is a list, then labels and flows must have the "
                "same length.\nlabels has length %d, but flows has length %d."
                % (len(labels), n))
        else:
            labels = [labels] * n
        if trunklength < 0:
            raise ValueError(
            "trunklength is negative.\nThis isn't allowed, because it would "
            "cause poor layout.")
        if np.abs(np.sum(flows)) > self.tolerance:
            _log.info("The sum of the flows is nonzero (%f).\nIs the "
                     "system not at steady state?", np.sum(flows))
        scaled_flows = self.scale * flows
        gain = sum(max(flow, 0) for flow in scaled_flows)
        loss = sum(min(flow, 0) for flow in scaled_flows)
        if not (0.5 <= gain <= 2.0):
            _log.info(
                "The scaled sum of the inputs is %f.\nThis may "
                "cause poor layout.\nConsider changing the scale so"
                " that the scaled sum is approximately 1.0.", gain)
        if not (-2.0 <= loss <= -0.5):
            _log.info(
                "The scaled sum of the outputs is %f.\nThis may "
                "cause poor layout.\nConsider changing the scale so"
                " that the scaled sum is approximately 1.0.", gain)
        if prior is not None:
            if prior < 0:
                raise ValueError("The index of the prior diagram is negative.")
            if min(connect) < 0:
                raise ValueError(
                "At least one of the connection indices is negative.")
            if prior >= len(self.diagrams):
                raise ValueError(
                "The index of the prior diagram is %d, but there are "
                "only %d other diagrams.\nThe index is zero-based."
                % (prior, len(self.diagrams)))
            if connect[0] >= len(self.diagrams[prior].flows):
                raise ValueError(
                "The connection index to the source diagram is %d, but "
                "that diagram has only %d flows.\nThe index is zero-based."
                % (connect[0], len(self.diagrams[prior].flows)))
            if connect[1] >= n:
                raise ValueError(
                "The connection index to this diagram is %d, but this diagram"
                "has only %d flows.\n The index is zero-based."
                % (connect[1], n))
            if self.diagrams[prior].angles[connect[0]] is None:
                raise ValueError(
                "The connection cannot be made.  Check that the magnitude "
                "of flow %d of diagram %d is greater than or equal to the "
                "specified tolerance." % (connect[0], prior))
            flow_error = (self.diagrams[prior].flows[connect[0]] +
                          flows[connect[1]])
            if abs(flow_error) >= self.tolerance:
                raise ValueError(
                "The scaled sum of the connected flows is %f, which is not "
                "within the tolerance (%f)." % (flow_error, self.tolerance))

        # Determine if the flows are inputs.
        are_inputs = [None] * n
        for i, flow in enumerate(flows):
            if flow >= self.tolerance:
                are_inputs[i] = True
            elif flow <= -self.tolerance:
                are_inputs[i] = False
            else:
                _log.info(
                    "The magnitude of flow %d (%f) is below the "
                    "tolerance (%f).\nIt will not be shown, and it "
                    "cannot be used in a connection."
                    % (i, flow, self.tolerance))

        # Determine the angles of the arrows (before rotation).
        angles = [None] * n
        for i, (orient, is_input) in enumerate(zip(orientations, are_inputs)):
            if orient == 1:
                if is_input:
                    angles[i] = DOWN
                elif not is_input:
                    # Be specific since is_input can be None.
                    angles[i] = UP
            elif orient == 0:
                if is_input is not None:
                    angles[i] = RIGHT
            else:
                if orient != -1:
                    raise ValueError(
                    "The value of orientations[%d] is %d, "
                    "but it must be [ -1 | 0 | 1 ]." % (i, orient))
                if is_input:
                    angles[i] = UP
                elif not is_input:
                    angles[i] = DOWN

        # Justify the lengths of the paths.
        if iterable(pathlengths):
            if len(pathlengths) != n:
                raise ValueError(
                "If pathlengths is a list, then pathlengths and flows must "
                "have the same length.\npathlengths has length %d, but flows "
                "has length %d." % (len(pathlengths), n))
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
                elif angle == UP and not is_input:
                    pathlengths[i] = urlength
                    urlength -= flow  # Flow is negative for outputs.
            # Determine the lengths of the bottom-side arrows
            # from the middle outwards.
            for i, (angle, is_input, flow) in enumerate(reversed(list(zip(
                  angles, are_inputs, scaled_flows)))):
                if angle == UP and is_input:
                    pathlengths[n - i - 1] = lllength
                    lllength += flow
                elif angle == DOWN and not is_input:
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
                    if not is_input:
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
            elif angle == UP and not is_input:
                tips[i, :], label_locations[i, :] = self._add_output(
                    urpath, angle, *spec)
        # Add the bottom-side inputs and outputs from the middle outwards.
        for i, (angle, is_input, spec) in enumerate(reversed(list(zip(
              angles, are_inputs, list(zip(scaled_flows, pathlengths)))))):
            if angle == UP and is_input:
                tip, label_location = self._add_input(llpath, angle, *spec)
                tips[n - i - 1, :] = tip
                label_locations[n - i - 1, :] = label_location
            elif angle == DOWN and not is_input:
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
            if angle == RIGHT and not is_input:
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
        if rcParams['_internal.classic_mode']:
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
                quantity = self.format % abs(number) + self.unit
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
