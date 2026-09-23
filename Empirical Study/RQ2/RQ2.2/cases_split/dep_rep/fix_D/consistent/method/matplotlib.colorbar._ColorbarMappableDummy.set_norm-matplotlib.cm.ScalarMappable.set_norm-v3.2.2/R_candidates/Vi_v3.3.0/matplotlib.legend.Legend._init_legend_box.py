    def _init_legend_box(self, handles, labels, markerfirst=True):
        """
        Initialize the legend_box. The legend_box is an instance of
        the OffsetBox, which is packed with legend handles and
        texts. Once packed, their location is calculated during the
        drawing time.
        """

        fontsize = self._fontsize

        # legend_box is a HPacker, horizontally packed with
        # columns. Each column is a VPacker, vertically packed with
        # legend items. Each legend item is HPacker packed with
        # legend handleBox and labelBox. handleBox is an instance of
        # offsetbox.DrawingArea which contains legend handle. labelBox
        # is an instance of offsetbox.TextArea which contains legend
        # text.

        text_list = []  # the list of text instances
        handle_list = []  # the list of text instances
        handles_and_labels = []

        label_prop = dict(verticalalignment='baseline',
                          horizontalalignment='left',
                          fontproperties=self.prop,
                          )

        # The approximate height and descent of text. These values are
        # only used for plotting the legend handle.
        descent = 0.35 * fontsize * (self.handleheight - 0.7)
        # 0.35 and 0.7 are just heuristic numbers and may need to be improved.
        height = fontsize * self.handleheight - descent
        # each handle needs to be drawn inside a box of (x, y, w, h) =
        # (0, -descent, width, height).  And their coordinates should
        # be given in the display coordinates.

        # The transformation of each handle will be automatically set
        # to self.get_transform(). If the artist does not use its
        # default transform (e.g., Collections), you need to
        # manually set their transform to the self.get_transform().
        legend_handler_map = self.get_legend_handler_map()

        for orig_handle, lab in zip(handles, labels):
            handler = self.get_legend_handler(legend_handler_map, orig_handle)
            if handler is None:
                cbook._warn_external(
                    "Legend does not support {!r} instances.\nA proxy artist "
                    "may be used instead.\nSee: "
                    "https://matplotlib.org/users/legend_guide.html"
                    "#creating-artists-specifically-for-adding-to-the-legend-"
                    "aka-proxy-artists".format(orig_handle))
                # We don't have a handle for this artist, so we just defer
                # to None.
                handle_list.append(None)
            else:
                textbox = TextArea(lab, textprops=label_prop,
                                   multilinebaseline=True,
                                   minimumdescent=True)
                handlebox = DrawingArea(width=self.handlelength * fontsize,
                                        height=height,
                                        xdescent=0., ydescent=descent)

                text_list.append(textbox._text)
                # Create the artist for the legend which represents the
                # original artist/handle.
                handle_list.append(handler.legend_artist(self, orig_handle,
                                                         fontsize, handlebox))
                handles_and_labels.append((handlebox, textbox))

        if handles_and_labels:
            # We calculate number of rows in each column. The first
            # (num_largecol) columns will have (nrows+1) rows, and remaining
            # (num_smallcol) columns will have (nrows) rows.
            ncol = min(self._ncol, len(handles_and_labels))
            nrows, num_largecol = divmod(len(handles_and_labels), ncol)
            num_smallcol = ncol - num_largecol
            # starting index of each column and number of rows in it.
            rows_per_col = [nrows + 1] * num_largecol + [nrows] * num_smallcol
            start_idxs = np.concatenate([[0], np.cumsum(rows_per_col)[:-1]])
            cols = zip(start_idxs, rows_per_col)
        else:
            cols = []

        columnbox = []
        for i0, di in cols:
            # pack handleBox and labelBox into itemBox
            itemBoxes = [HPacker(pad=0,
                                 sep=self.handletextpad * fontsize,
                                 children=[h, t] if markerfirst else [t, h],
                                 align="baseline")
                         for h, t in handles_and_labels[i0:i0 + di]]
            # minimumdescent=False for the text of the last row of the column
            if markerfirst:
                itemBoxes[-1].get_children()[1].set_minimumdescent(False)
            else:
                itemBoxes[-1].get_children()[0].set_minimumdescent(False)

            # pack columnBox
            alignment = "baseline" if markerfirst else "right"
            columnbox.append(VPacker(pad=0,
                                     sep=self.labelspacing * fontsize,
                                     align=alignment,
                                     children=itemBoxes))

        mode = "expand" if self._mode == "expand" else "fixed"
        sep = self.columnspacing * fontsize
        self._legend_handle_box = HPacker(pad=0,
                                          sep=sep, align="baseline",
                                          mode=mode,
                                          children=columnbox)
        self._legend_title_box = TextArea("")
        self._legend_box = VPacker(pad=self.borderpad * fontsize,
                                   sep=self.labelspacing * fontsize,
                                   align="center",
                                   children=[self._legend_title_box,
                                             self._legend_handle_box])
        self._legend_box.set_figure(self.figure)
        self.texts = text_list
        self.legendHandles = handle_list
