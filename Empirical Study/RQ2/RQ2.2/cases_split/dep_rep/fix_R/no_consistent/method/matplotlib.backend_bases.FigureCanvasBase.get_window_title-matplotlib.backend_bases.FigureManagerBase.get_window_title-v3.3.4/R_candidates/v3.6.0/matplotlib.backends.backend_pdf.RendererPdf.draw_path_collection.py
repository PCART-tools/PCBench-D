    def draw_path_collection(self, gc, master_transform, paths, all_transforms,
                             offsets, offset_trans, facecolors, edgecolors,
                             linewidths, linestyles, antialiaseds, urls,
                             offset_position):
        # We can only reuse the objects if the presence of fill and
        # stroke (and the amount of alpha for each) is the same for
        # all of them
        can_do_optimization = True
        facecolors = np.asarray(facecolors)
        edgecolors = np.asarray(edgecolors)

        if not len(facecolors):
            filled = False
            can_do_optimization = not gc.get_hatch()
        else:
            if np.all(facecolors[:, 3] == facecolors[0, 3]):
                filled = facecolors[0, 3] != 0.0
            else:
                can_do_optimization = False

        if not len(edgecolors):
            stroked = False
        else:
            if np.all(np.asarray(linewidths) == 0.0):
                stroked = False
            elif np.all(edgecolors[:, 3] == edgecolors[0, 3]):
                stroked = edgecolors[0, 3] != 0.0
            else:
                can_do_optimization = False

        # Is the optimization worth it? Rough calculation:
        # cost of emitting a path in-line is len_path * uses_per_path
        # cost of XObject is len_path + 5 for the definition,
        #    uses_per_path for the uses
        len_path = len(paths[0].vertices) if len(paths) > 0 else 0
        uses_per_path = self._iter_collection_uses_per_path(
            paths, all_transforms, offsets, facecolors, edgecolors)
        should_do_optimization = \
            len_path + uses_per_path + 5 < len_path * uses_per_path

        if (not can_do_optimization) or (not should_do_optimization):
            return RendererBase.draw_path_collection(
                self, gc, master_transform, paths, all_transforms,
                offsets, offset_trans, facecolors, edgecolors,
                linewidths, linestyles, antialiaseds, urls,
                offset_position)

        padding = np.max(linewidths)
        path_codes = []
        for i, (path, transform) in enumerate(self._iter_collection_raw_paths(
                master_transform, paths, all_transforms)):
            name = self.file.pathCollectionObject(
                gc, path, transform, padding, filled, stroked)
            path_codes.append(name)

        output = self.file.output
        output(*self.gc.push())
        lastx, lasty = 0, 0
        for xo, yo, path_id, gc0, rgbFace in self._iter_collection(
                gc, path_codes, offsets, offset_trans,
                facecolors, edgecolors, linewidths, linestyles,
                antialiaseds, urls, offset_position):

            self.check_gc(gc0, rgbFace)
            dx, dy = xo - lastx, yo - lasty
            output(1, 0, 0, 1, dx, dy, Op.concat_matrix, path_id,
                   Op.use_xobject)
            lastx, lasty = xo, yo
        output(*self.gc.pop())
