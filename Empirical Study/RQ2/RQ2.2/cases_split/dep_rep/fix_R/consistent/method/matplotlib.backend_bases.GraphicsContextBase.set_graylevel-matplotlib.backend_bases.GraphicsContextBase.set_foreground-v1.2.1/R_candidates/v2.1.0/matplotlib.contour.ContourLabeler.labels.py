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
            lw *= self.ax.figure.dpi / 72.0  # scale to screen coordinates
            additions = []
            paths = con.get_paths()
            for segNum, linepath in enumerate(paths):
                lc = linepath.vertices  # Line contour
                slc0 = trans.transform(lc)  # Line contour in screen coords

                # For closed polygons, add extra point to avoid division by
                # zero in print_label and locate_label.  Other than these
                # functions, this is not necessary and should probably be
                # eventually removed.
                if mlab.is_closed_polygon(lc):
                    slc = np.r_[slc0, slc0[1:2, :]]
                else:
                    slc = slc0

                # Check if long enough for a label
                if self.print_label(slc, lw):
                    x, y, ind = self.locate_label(slc, lw)

                    if inline:
                        lcarg = lc
                    else:
                        lcarg = None
                    rotation, new = self.calc_label_rot_and_inline(
                        slc0, ind, lw, lcarg,
                        inline_spacing)

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

            # After looping over all segments on a contour, remove old
            # paths and add new ones if inlining
            if inline:
                del paths[:]
                paths.extend(additions)
