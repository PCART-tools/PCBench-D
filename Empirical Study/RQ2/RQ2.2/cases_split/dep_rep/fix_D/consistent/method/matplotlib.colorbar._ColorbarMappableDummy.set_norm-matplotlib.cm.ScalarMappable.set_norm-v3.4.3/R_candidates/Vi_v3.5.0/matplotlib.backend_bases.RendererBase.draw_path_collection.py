    def draw_path_collection(self, gc, master_transform, paths, all_transforms,
                             offsets, offsetTrans, facecolors, edgecolors,
                             linewidths, linestyles, antialiaseds, urls,
                             offset_position):
        """
        Draw a collection of paths selecting drawing properties from
        the lists *facecolors*, *edgecolors*, *linewidths*,
        *linestyles* and *antialiaseds*. *offsets* is a list of
        offsets to apply to each of the paths.  The offsets in
        *offsets* are first transformed by *offsetTrans* before being
        applied.

        *offset_position* is unused now, but the argument is kept for
        backwards compatibility.

        This provides a fallback implementation of
        :meth:`draw_path_collection` that makes multiple calls to
        :meth:`draw_path`.  Some backends may want to override this in
        order to render each set of path data only once, and then
        reference that path multiple times with the different offsets,
        colors, styles etc.  The generator methods
        :meth:`_iter_collection_raw_paths` and
        :meth:`_iter_collection` are provided to help with (and
        standardize) the implementation across backends.  It is highly
        recommended to use those generators, so that changes to the
        behavior of :meth:`draw_path_collection` can be made globally.
        """
        path_ids = self._iter_collection_raw_paths(master_transform,
                                                   paths, all_transforms)

        for xo, yo, path_id, gc0, rgbFace in self._iter_collection(
                gc, master_transform, all_transforms, list(path_ids), offsets,
                offsetTrans, facecolors, edgecolors, linewidths, linestyles,
                antialiaseds, urls, offset_position):
            path, transform = path_id
            # Only apply another translation if we have an offset, else we
            # reuse the initial transform.
            if xo != 0 or yo != 0:
                # The transformation can be used by multiple paths. Since
                # translate is a inplace operation, we need to copy the
                # transformation by .frozen() before applying the translation.
                transform = transform.frozen()
                transform.translate(xo, yo)
            self.draw_path(gc0, path, transform, rgbFace)
