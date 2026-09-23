    def draw_text(self, gc, x, y, s, prop, angle, ismath=False, mtext=None):
        # docstring inherited

        clip_attrs = self._get_clip_attrs(gc)
        if clip_attrs:
            # Cannot apply clip-path directly to the text, because
            # it has a transformation
            self.writer.start('g', **clip_attrs)

        if gc.get_url() is not None:
            self.writer.start('a', {'xlink:href': gc.get_url()})

        if mpl.rcParams['svg.fonttype'] == 'path':
            self._draw_text_as_path(gc, x, y, s, prop, angle, ismath, mtext)
        else:
            self._draw_text_as_text(gc, x, y, s, prop, angle, ismath, mtext)

        if gc.get_url() is not None:
            self.writer.end('a')

        if clip_attrs:
            self.writer.end('g')
