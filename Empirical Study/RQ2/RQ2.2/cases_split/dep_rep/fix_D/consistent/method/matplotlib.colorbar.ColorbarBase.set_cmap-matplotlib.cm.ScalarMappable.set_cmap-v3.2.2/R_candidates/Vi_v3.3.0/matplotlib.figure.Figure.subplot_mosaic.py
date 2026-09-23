    def subplot_mosaic(self, layout, *, subplot_kw=None, gridspec_kw=None,
                       empty_sentinel='.'):
        """
        Build a layout of Axes based on ASCII art or nested lists.

        This is a helper function to build complex GridSpec layouts visually.

        .. note ::

           This API is provisional and may be revised in the future based on
           early user feedback.


        Parameters
        ----------
        layout : list of list of {hashable or nested} or str

            A visual layout of how you want your Axes to be arranged
            labeled as strings.  For example ::

               x = [['A panel', 'A panel', 'edge'],
                    ['C panel', '.',       'edge']]

            Produces 4 axes:

            - 'A panel' which is 1 row high and spans the first two columns
            - 'edge' which is 2 rows high and is on the right edge
            - 'C panel' which in 1 row and 1 column wide in the bottom left
            - a blank space 1 row and 1 column wide in the bottom center

            Any of the entries in the layout can be a list of lists
            of the same form to create nested layouts.

            If input is a str, then it must be of the form ::

              '''
              AAE
              C.E
              '''

            where each character is a column and each line is a row.
            This only allows only single character Axes labels and does
            not allow nesting but is very terse.

        subplot_kw : dict, optional
            Dictionary with keywords passed to the `.Figure.add_subplot` call
            used to create each subplot.

        gridspec_kw : dict, optional
            Dictionary with keywords passed to the `.GridSpec` constructor used
            to create the grid the subplots are placed on.

        empty_sentinel : object, optional
            Entry in the layout to mean "leave this space empty".  Defaults
            to ``'.'``. Note, if *layout* is a string, it is processed via
            `inspect.cleandoc` to remove leading white space, which may
            interfere with using white-space as the empty sentinel.

        Returns
        -------
        dict[label, Axes]
           A dictionary mapping the labels to the Axes objects.

        """
        subplot_kw = subplot_kw or {}
        gridspec_kw = gridspec_kw or {}
        # special-case string input
        if isinstance(layout, str):
            layout = self._normalize_grid_string(layout)

        def _make_array(inp):
            """
            Convert input into 2D array

            We need to have this internal function rather than
            ``np.asarray(..., dtype=object)`` so that a list of lists
            of lists does not get converted to an array of dimension >
            2

            Returns
            -------
            2D object array

            """
            r0, *rest = inp
            for j, r in enumerate(rest, start=1):
                if isinstance(r, str):
                    raise ValueError('List layout specification must be 2D')
                if len(r0) != len(r):
                    raise ValueError(
                        "All of the rows must be the same length, however "
                        f"the first row ({r0!r}) has length {len(r0)} "
                        f"and row {j} ({r!r}) has length {len(r)}."
                    )
            out = np.zeros((len(inp), len(r0)), dtype=object)
            for j, r in enumerate(inp):
                for k, v in enumerate(r):
                    out[j, k] = v
            return out

        def _identify_keys_and_nested(layout):
            """
            Given a 2D object array, identify unique IDs and nested layouts

            Parameters
            ----------
            layout : 2D numpy object array

            Returns
            -------
            unique_ids : Set[object]
                The unique non-sub layout entries in this layout
            nested : Dict[Tuple[int, int]], 2D object array
            """
            unique_ids = set()
            nested = {}
            for j, row in enumerate(layout):
                for k, v in enumerate(row):
                    if v == empty_sentinel:
                        continue
                    elif not cbook.is_scalar_or_string(v):
                        nested[(j, k)] = _make_array(v)
                    else:
                        unique_ids.add(v)

            return unique_ids, nested

        def _do_layout(gs, layout, unique_ids, nested):
            """
            Recursively do the layout.

            Parameters
            ----------
            gs : GridSpec

            layout : 2D object array
                The input converted to a 2D numpy array for this level.

            unique_ids : Set[object]
                The identified scalar labels at this level of nesting.

            nested : Dict[Tuple[int, int]], 2D object array
                The identified nested layouts if any.

            Returns
            -------
            Dict[label, Axes]
                A flat dict of all of the Axes created.
            """
            rows, cols = layout.shape
            output = dict()

            # create the Axes at this level of nesting
            for name in unique_ids:
                indx = np.argwhere(layout == name)
                start_row, start_col = np.min(indx, axis=0)
                end_row, end_col = np.max(indx, axis=0) + 1
                slc = (slice(start_row, end_row), slice(start_col, end_col))

                if (layout[slc] != name).any():
                    raise ValueError(
                        f"While trying to layout\n{layout!r}\n"
                        f"we found that the label {name!r} specifies a "
                        "non-rectangular or non-contiguous area.")

                ax = self.add_subplot(
                    gs[slc], **{'label': str(name), **subplot_kw}
                )
                output[name] = ax

            # do any sub-layouts
            for (j, k), nested_layout in nested.items():
                rows, cols = nested_layout.shape
                nested_output = _do_layout(
                    gs[j, k].subgridspec(rows, cols, **gridspec_kw),
                    nested_layout,
                    *_identify_keys_and_nested(nested_layout)
                )
                overlap = set(output) & set(nested_output)
                if overlap:
                    raise ValueError(f"There are duplicate keys {overlap} "
                                     f"between the outer layout\n{layout!r}\n"
                                     f"and the nested layout\n{nested_layout}")
                output.update(nested_output)
            return output

        layout = _make_array(layout)
        rows, cols = layout.shape
        gs = self.add_gridspec(rows, cols, **gridspec_kw)
        ret = _do_layout(gs, layout, *_identify_keys_and_nested(layout))
        for k, ax in ret.items():
            if isinstance(k, str):
                ax.set_label(k)
        return ret
