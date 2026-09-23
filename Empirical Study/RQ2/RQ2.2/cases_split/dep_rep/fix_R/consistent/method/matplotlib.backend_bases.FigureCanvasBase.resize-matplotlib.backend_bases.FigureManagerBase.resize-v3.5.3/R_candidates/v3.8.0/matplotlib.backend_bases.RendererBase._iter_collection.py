    def _iter_collection(self, gc, path_ids, offsets, offset_trans, facecolors,
                         edgecolors, linewidths, linestyles,
                         antialiaseds, urls, offset_position):
        """
        Helper method (along with `_iter_collection_raw_paths`) to implement
        `draw_path_collection` in a memory-efficient manner.

        This method yields all of the path, offset and graphics context
        combinations to draw the path collection.  The caller should already
        have looped over the results of `_iter_collection_raw_paths` to draw
        this collection.

        The arguments should be the same as that passed into
        `draw_path_collection`, with the exception of *path_ids*, which is a
        list of arbitrary objects that the backend will use to reference one of
        the paths created in the `_iter_collection_raw_paths` stage.

        Each yielded result is of the form::

           xo, yo, path_id, gc, rgbFace

        where *xo*, *yo* is an offset; *path_id* is one of the elements of
        *path_ids*; *gc* is a graphics context and *rgbFace* is a color to
        use for filling the path.
        """
        Npaths = len(path_ids)
        Noffsets = len(offsets)
        N = max(Npaths, Noffsets)
        Nfacecolors = len(facecolors)
        Nedgecolors = len(edgecolors)
        Nlinewidths = len(linewidths)
        Nlinestyles = len(linestyles)
        Nurls = len(urls)

        if (Nfacecolors == 0 and Nedgecolors == 0) or Npaths == 0:
            return

        gc0 = self.new_gc()
        gc0.copy_properties(gc)

        def cycle_or_default(seq, default=None):
            # Cycle over *seq* if it is not empty; else always yield *default*.
            return (itertools.cycle(seq) if len(seq)
                    else itertools.repeat(default))

        pathids = cycle_or_default(path_ids)
        toffsets = cycle_or_default(offset_trans.transform(offsets), (0, 0))
        fcs = cycle_or_default(facecolors)
        ecs = cycle_or_default(edgecolors)
        lws = cycle_or_default(linewidths)
        lss = cycle_or_default(linestyles)
        aas = cycle_or_default(antialiaseds)
        urls = cycle_or_default(urls)

        if Nedgecolors == 0:
            gc0.set_linewidth(0.0)

        for pathid, (xo, yo), fc, ec, lw, ls, aa, url in itertools.islice(
                zip(pathids, toffsets, fcs, ecs, lws, lss, aas, urls), N):
            if not (np.isfinite(xo) and np.isfinite(yo)):
                continue
            if Nedgecolors:
                if Nlinewidths:
                    gc0.set_linewidth(lw)
                if Nlinestyles:
                    gc0.set_dashes(*ls)
                if len(ec) == 4 and ec[3] == 0.0:
                    gc0.set_linewidth(0)
                else:
                    gc0.set_foreground(ec)
            if fc is not None and len(fc) == 4 and fc[3] == 0:
                fc = None
            gc0.set_antialiased(aa)
            if Nurls:
                gc0.set_url(url)
            yield xo, yo, pathid, gc0, fc
        gc0.restore()
