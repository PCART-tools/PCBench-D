    def draw_path_collection(self, gc, master_transform, paths, all_transforms,
                             offsets, offsetTrans, facecolors, edgecolors,
                             linewidths, linestyles, antialiaseds, urls,
                             offset_position):
        # Is the optimization worth it? Rough calculation:
        # cost of emitting a path in-line is
        #    (len_path + 5) * uses_per_path
        # cost of definition+use is
        #    (len_path + 3) + 9 * uses_per_path
        len_path = len(paths[0].vertices) if len(paths) > 0 else 0
        uses_per_path = self._iter_collection_uses_per_path(
            paths, all_transforms, offsets, facecolors, edgecolors)
        should_do_optimization = \
            len_path + 9 * uses_per_path + 3 < (len_path + 5) * uses_per_path
        if not should_do_optimization:
            return super().draw_path_collection(
                gc, master_transform, paths, all_transforms,
                offsets, offsetTrans, facecolors, edgecolors,
                linewidths, linestyles, antialiaseds, urls,
                offset_position)

        writer = self.writer
        path_codes = []
        writer.start('defs')
        for i, (path, transform) in enumerate(self._iter_collection_raw_paths(
                master_transform, paths, all_transforms)):
            transform = Affine2D(transform.get_matrix()).scale(1.0, -1.0)
            d = self._convert_path(path, transform, simplify=False)
            oid = 'C%x_%x_%s' % (
                self._path_collection_id, i, self._make_id('', d))
            writer.element('path', id=oid, d=d)
            path_codes.append(oid)
        writer.end('defs')

        for xo, yo, path_id, gc0, rgbFace in self._iter_collection(
                gc, master_transform, all_transforms, path_codes, offsets,
                offsetTrans, facecolors, edgecolors, linewidths, linestyles,
                antialiaseds, urls, offset_position):
            url = gc0.get_url()
            if url is not None:
                writer.start('a', attrib={'xlink:href': url})
            clip_attrs = self._get_clip_attrs(gc0)
            if clip_attrs:
                writer.start('g', **clip_attrs)
            attrib = {
                'xlink:href': '#%s' % path_id,
                'x': short_float_fmt(xo),
                'y': short_float_fmt(self.height - yo),
                'style': self._get_style(gc0, rgbFace)
                }
            writer.element('use', attrib=attrib)
            if clip_attrs:
                writer.end('g')
            if url is not None:
                writer.end('a')

        self._path_collection_id += 1
