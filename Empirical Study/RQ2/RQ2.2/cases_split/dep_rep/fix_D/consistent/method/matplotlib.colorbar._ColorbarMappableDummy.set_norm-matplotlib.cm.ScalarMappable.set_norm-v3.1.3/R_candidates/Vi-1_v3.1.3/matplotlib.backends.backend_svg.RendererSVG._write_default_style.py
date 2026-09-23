    def _write_default_style(self):
        writer = self.writer
        default_style = generate_css({
            'stroke-linejoin': 'round',
            'stroke-linecap': 'butt'})
        writer.start('defs')
        writer.start('style', type='text/css')
        writer.data('*{%s}\n' % default_style)
        writer.end('style')
        writer.end('defs')
