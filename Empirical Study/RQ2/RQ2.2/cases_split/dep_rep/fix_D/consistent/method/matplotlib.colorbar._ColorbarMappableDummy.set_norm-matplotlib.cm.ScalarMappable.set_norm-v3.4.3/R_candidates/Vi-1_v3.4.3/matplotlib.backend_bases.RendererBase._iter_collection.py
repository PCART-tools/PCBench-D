    def _iter_collection(self, gc, master_transform, all_transforms,
                         path_ids, offsets, offsetTrans, facecolors,
                         edgecolors, linewidths, linestyles,
                         antialiaseds, urls, offset_position):
        """
        Helper method (along with :meth:`_iter_collection_raw_paths`) to
        implement :meth:`draw_path_collection` in a space-efficient manner.

        This method yields all of the path, offset and graphics
        context combinations to draw the path collection.  The caller
        should already have looped over the results of
        :meth:`_iter_collection_raw_paths` to draw this collection.

        The arguments should be the same as that passed into
        :meth:`draw_path_collection`, with the exception of
        *path_ids*, which is a list of arbitrary objects that the
        backend will use to reference one of the paths created in the
        :meth:`_iter_collection_raw_paths` stage.

        Each yielded result is of the form::

           xo, yo, path_id, gc, rgbFace

        where *xo*, *yo* is an offset; *path_id* is one of the elements of
        *path_ids*; *gc* is a graphics context and *rgbFace* is a color to
        use for filling the path.
        """
        Ntransforms = len(all_transforms)
        Npaths = len(path_ids)
        Noffsets = len(offsets)
        N = max(Npaths, Noffsets)
        Nfacecolors = len(facecolors)
        Nedgecolors = len(edgecolors)
        Nlinewidths = len(linewidths)
        Nlinestyles = len(linestyles)
        Naa = len(antialiaseds)
        Nurls = len(urls)

        if offset_position == "data":
            _api.warn_deprecated(
                "3.3", message="Support for offset_position='data' is "
                "deprecated since %(since)s and will be removed %(removal)s.")

        if (Nfacecolors == 0 and Nedgecolors == 0) or Npaths == 0:
            return
        if Noffsets:
            toffsets = offsetTrans.transform(offsets)

        gc0 = self.new_gc()
        gc0.copy_properties(gc)

        if Nfacecolors == 0:
            rgbFace = None

        if Nedgecolors == 0:
            gc0.set_linewidth(0.0)

        xo, yo = 0, 0
        for i in range(N):
            path_id = path_ids[i % Npaths]
            if Noffsets:
                xo, yo = toffsets[i % Noffsets]
                if offset_position == 'data':
                    if Ntransforms:
                        transform = (
                            Affine2D(all_transforms[i % Ntransforms]) +
                            master_transform)
                    else:
                        transform = master_transform
                    (xo, yo), (xp, yp) = transform.transform(
                        [(xo, yo), (0, 0)])
                    xo = -(xp - xo)
                    yo = -(yp - yo)
            if not (np.isfinite(xo) and np.isfinite(yo)):
                continue
            if Nfacecolors:
                rgbFace = facecolors[i % Nfacecolors]
            if Nedgecolors:
                if Nlinewidths:
                    gc0.set_linewidth(linewidths[i % Nlinewidths])
                if Nlinestyles:
                    gc0.set_dashes(*linestyles[i % Nlinestyles])
                fg = edgecolors[i % Nedgecolors]
                if len(fg) == 4:
                    if fg[3] == 0.0:
                        gc0.set_linewidth(0)
                    else:
                        gc0.set_foreground(fg)
                else:
                    gc0.set_foreground(fg)
            if rgbFace is not None and len(rgbFace) == 4:
                if rgbFace[3] == 0:
                    rgbFace = None
            gc0.set_antialiased(antialiaseds[i % Naa])
            if Nurls:
                gc0.set_url(urls[i % Nurls])

            yield xo, yo, path_id, gc0, rgbFace
        gc0.restore()
