    def labels(self, inline, inline_spacing):

        if self._use_clabeltext:
            add_label = self.add_label_clabeltext
        else:
            add_label = self.add_label

        for icon, lev, fsize, cvalue in zip(
                self.labelIndiceList, self.labelLevelList,
                self.labelFontSizeList, self.labelCValueList):

            con = self.collections[icon]
            trans = con.get_transform()
            lw = self.get_label_width(lev, self.labelFmt, fsize)
            lw *= self.axes.figure.dpi / 72  # scale to screen coordinates
            additions = []
            paths = con.get_paths()
            for segNum, linepath in enumerate(paths):
                lc = linepath.vertices  # Line contour
                slc = trans.transform(lc)  # Line contour in screen coords

                # Check if long enough for a label
                if self.print_label(slc, lw):
                    x, y, ind = self.locate_label(slc, lw)

                    rotation, new = self.calc_label_rot_and_inline(
                        slc, ind, lw, lc if inline else None, inline_spacing)

                    # Actually add the label
                    add_label(x, y, rotation, lev, cvalue)

                    # If inline, add new contours
                    if inline:
                        for n in new:
                            # Add path if not empty or single point
                            if len(n) > 1:
                                additions.append(mpath.Path(n))
                else:  # If not adding label, keep old path
                    additions.append(linepath)

            # After looping over all segments on a contour, replace old paths
            # by new ones if inlining.
            if inline:
                paths[:] = additions
