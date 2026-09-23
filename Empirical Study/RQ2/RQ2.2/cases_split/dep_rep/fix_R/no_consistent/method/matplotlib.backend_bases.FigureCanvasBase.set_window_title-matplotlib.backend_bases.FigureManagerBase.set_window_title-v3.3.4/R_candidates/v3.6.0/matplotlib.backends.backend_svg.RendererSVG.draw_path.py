    def draw_path(self, gc, path, transform, rgbFace=None):
        # docstring inherited
        trans_and_flip = self._make_flip_transform(transform)
        clip = (rgbFace is None and gc.get_hatch_path() is None)
        simplify = path.should_simplify and clip
        path_data = self._convert_path(
            path, trans_and_flip, clip=clip, simplify=simplify,
            sketch=gc.get_sketch_params())

        if gc.get_url() is not None:
            self.writer.start('a', {'xlink:href': gc.get_url()})
        self.writer.element('path', d=path_data, **self._get_clip_attrs(gc),
                            style=self._get_style(gc, rgbFace))
        if gc.get_url() is not None:
            self.writer.end('a')
