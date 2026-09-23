    def draw_text(self, gc, x, y, s, prop, angle, ismath=False, mtext=None):
        clipid = self._get_clip(gc)
        if clipid is not None:
            # Cannot apply clip-path directly to the text, because
            # is has a transformation
            self.writer.start(
                'g', attrib={'clip-path': 'url(#%s)' % clipid})

        if gc.get_url() is not None:
            self.writer.start('a', {'xlink:href': gc.get_url()})

        if rcParams['svg.fonttype'] == 'path':
            self._draw_text_as_path(gc, x, y, s, prop, angle, ismath, mtext)
        else:
            self._draw_text_as_text(gc, x, y, s, prop, angle, ismath, mtext)

        if gc.get_url() is not None:
            self.writer.end('a')

        if clipid is not None:
            self.writer.end('g')
