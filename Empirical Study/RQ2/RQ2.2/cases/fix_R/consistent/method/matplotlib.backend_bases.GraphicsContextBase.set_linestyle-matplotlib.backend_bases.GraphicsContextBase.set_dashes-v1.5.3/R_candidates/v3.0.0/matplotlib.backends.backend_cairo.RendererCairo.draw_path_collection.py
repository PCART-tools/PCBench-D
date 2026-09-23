    def draw_path_collection(
            self, gc, master_transform, paths, all_transforms, offsets,
            offsetTrans, facecolors, edgecolors, linewidths, linestyles,
            antialiaseds, urls, offset_position):

        path_ids = []
        for path, transform in self._iter_collection_raw_paths(
                master_transform, paths, all_transforms):
            path_ids.append((path, Affine2D(transform)))

        reuse_key = None
        grouped_draw = []

        def _draw_paths():
            if not grouped_draw:
                return
            gc_vars, rgb_fc = reuse_key
            gc = copy.copy(gc0)
            # We actually need to call the setters to reset the internal state.
            vars(gc).update(gc_vars)
            for k, v in gc_vars.items():
                if k == "_linestyle":  # Deprecated, no effect.
                    continue
                try:
                    getattr(gc, "set" + k)(v)
                except (AttributeError, TypeError) as e:
                    pass
            gc.ctx.new_path()
            paths, transforms = zip(*grouped_draw)
            grouped_draw.clear()
            _append_paths(gc.ctx, paths, transforms)
            self._fill_and_stroke(
                gc.ctx, rgb_fc, gc.get_alpha(), gc.get_forced_alpha())

        for xo, yo, path_id, gc0, rgb_fc in self._iter_collection(
                gc, master_transform, all_transforms, path_ids, offsets,
                offsetTrans, facecolors, edgecolors, linewidths, linestyles,
                antialiaseds, urls, offset_position):
            path, transform = path_id
            transform = (Affine2D(transform.get_matrix())
                         .translate(xo, yo - self.height).scale(1, -1))
            # rgb_fc could be a ndarray, for which equality is elementwise.
            new_key = vars(gc0), tuple(rgb_fc) if rgb_fc is not None else None
            if new_key == reuse_key:
                grouped_draw.append((path, transform))
            else:
                _draw_paths()
                grouped_draw.append((path, transform))
                reuse_key = new_key
        _draw_paths()
